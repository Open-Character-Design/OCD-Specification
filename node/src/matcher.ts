/** Matcher module for compiling rule path selectors. */

import { JSONPath } from 'jsonpath-plus';

export interface PathMatch {
  value: any;
  path: string;
  context: Record<string, any>;
}

export class PathMatcher {
  private compiledPaths = new Map<string, any>();

  compilePath(path: string): any {
    if (!this.compiledPaths.has(path)) {
      // Convert OCD path syntax to JSONPath
      const jsonpathStr = this.convertToJsonpath(path);
      this.compiledPaths.set(path, (JSONPath as any).parse(jsonpathStr));
    }

    return this.compiledPaths.get(path)!;
  }

  private convertToJsonpath(path: string): string {
    // Handle root path
    if (path === '' || path === '.') {
      return '$';
    }

    // Split by dots and process each segment
    const segments = path.split('.');
    const jsonpathSegments = ['$'];

    for (const segment of segments) {
      if (segment === '') {
        continue;
      }

      // Handle array notation
      if (segment.includes('[]')) {
        // Convert "field[]" to "field[*]"
        const processedSegment = segment.replace(/\[\]/g, '[*]');
        jsonpathSegments.push(`.${processedSegment}`);
      } else if (segment === '[*]') {
        jsonpathSegments.push('[*]');
      } else if (segment.endsWith('[*]')) {
        const fieldName = segment.slice(0, -3);
        jsonpathSegments.push(`.${fieldName}[*]`);
      } else {
        jsonpathSegments.push(`.${segment}`);
      }
    }

    return jsonpathSegments.join('');
  }

  findMatches(document: any, path: string): PathMatch[] {
    try {
      const compiledPath = this.compilePath(path);
      const matches = compiledPath.find(document);

      return matches.map((match: any) => ({
        value: match.value,
        path: match.path.toString(),
        context: this.getContext(document, match.path)
      }));
    } catch (error) {
      // If path matching fails, return empty list
      return [];
    }
  }

  private getContext(document: any, fullPath: any): Record<string, any> {
    const context: Record<string, any> = {};

    try {
      // Get parent object
      if (fullPath.path && fullPath.path.length > 1) {
        const parentPath = new (JSONPath as any)(fullPath.path.slice(0, -1));
        const parentMatches = parentPath.find(document);
        if (parentMatches.length > 0) {
          context.parent = parentMatches[0].value;
        }
      }
    } catch {
      // Ignore context errors
    }

    return context;
  }

  pathExists(document: any, path: string): boolean {
    const matches = this.findMatches(document, path);
    return matches.length > 0;
  }

  getValueAtPath(document: any, path: string): any {
    const matches = this.findMatches(document, path);
    return matches.length > 0 ? matches[0].value : undefined;
  }

  validatePathSyntax(path: string): boolean {
    try {
      this.compilePath(path);
      return true;
    } catch {
      return false;
    }
  }

  getPathInfo(path: string): Record<string, any> {
    try {
      const compiledPath = this.compilePath(path);
      return {
        original: path,
        jsonpath: compiledPath.toString(),
        isArrayPath: compiledPath.toString().includes('[*]') || path.includes('[]'),
        isWildcard: path.endsWith('[*]') || path.endsWith('[]'),
        segments: path ? path.split('.') : []
      };
    } catch (error) {
      return {
        original: path,
        error: String(error),
        valid: false
      };
    }
  }
}
