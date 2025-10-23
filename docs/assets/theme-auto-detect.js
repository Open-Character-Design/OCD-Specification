/**
 * Simple theme auto-detection for MkDocs Material
 * Only detects system theme if user hasn't manually set a preference
 */
(function() {
  'use strict';

  const STORAGE_KEY = 'md-theme-preference';
  const THEME_ATTRIBUTE = 'data-md-color-scheme';
  const LIGHT_THEME = 'default';
  const DARK_THEME = 'slate';

  /**
   * Check if user has manually set a theme preference
   */
  function hasUserPreference() {
    try {
      return localStorage.getItem(STORAGE_KEY) !== null;
    } catch (e) {
      return false;
    }
  }

  /**
   * Get the system's preferred color scheme
   */
  function getSystemPreference() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  /**
   * Apply the theme to the document
   */
  function applyTheme(theme) {
    const html = document.documentElement;
    
    if (theme === 'dark') {
      html.setAttribute(THEME_ATTRIBUTE, DARK_THEME);
    } else {
      html.setAttribute(THEME_ATTRIBUTE, LIGHT_THEME);
    }
  }

  /**
   * Initialize theme based on system preference if no user preference exists
   */
  function initializeTheme() {
    // Only auto-detect if user hasn't manually set a preference
    if (!hasUserPreference()) {
      const systemTheme = getSystemPreference();
      applyTheme(systemTheme);
    }
  }

  /**
   * Handle system theme changes (only if no user preference)
   */
  function handleSystemThemeChange() {
    // Only auto-switch if user hasn't manually set a preference
    if (!hasUserPreference()) {
      const systemTheme = getSystemPreference();
      applyTheme(systemTheme);
    }
  }

  /**
   * Initialize the theme system
   */
  function init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initializeTheme);
    } else {
      initializeTheme();
    }

    // Listen for system theme changes
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      mediaQuery.addEventListener('change', handleSystemThemeChange);
    }
  }

  // Initialize
  init();

})();
