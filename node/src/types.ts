export type UUID = string;
export type Slug = string;

export interface LocalizedText {
  text: string;
  lang: string;
}

export type DisplayName = LocalizedText[] | Record<string, string>;

export interface Names {
  canon: string;
  display?: DisplayName;
  aliases?: string[];
  [key: string]: unknown;
}

export interface AgeMeasurement {
  value: number;
  unit: string;
}

export type Exposure = 'public' | 'secret';

export interface CompositeIdentityMember {
  ref: UUID;
  control_share: number;
  exposure: Exposure;
}

export interface SecretIdentity {
  public_name: string;
  exposure_risk: number;
  [key: string]: unknown;
}

export interface Identity {
  entity_kind: 'person' | 'collective' | 'creature' | 'object' | 'place' | 'abstract' | 'ai';
  species?: 'human' | 'ai' | 'alien' | 'collective' | 'object' | 'deity' | 'other';
  sapience_level: 'animal' | 'tool' | 'agent' | 'sapient' | 'transcendent';
  pronouns?: string[];
  age?: {
    nominal?: AgeMeasurement;
    biological?: AgeMeasurement;
    chronological?: AgeMeasurement;
    chrono_override?: AgeMeasurement;
    rationale?: string;
    [key: string]: unknown;
  };
  origins?: {
    universe?: string;
    birthplace?: string;
    debut_date?: string;
    [key: string]: unknown;
  };
  continuity?: {
    canon?: 'prime' | 'alt' | 'fanon' | 'apocrypha';
    timeline_ids?: UUID[];
    [key: string]: unknown;
  };
  roles?: Array<'protagonist' | 'antagonist' | 'support' | 'ensemble' | 'npc' | 'avatar'>;
  composite_of?: CompositeIdentityMember[];
  secret_identities?: SecretIdentity[];
  [key: string]: unknown;
}

export interface Creator {
  name: string;
  role?: string;
  [key: string]: unknown;
}

export interface Rights {
  owner?: string;
  license?: string;
  usage_notes?: string;
  [key: string]: unknown;
}

export interface Versioning {
  created_at: string;
  last_modified: string;
  change_log?: string[];
  [key: string]: unknown;
}

export interface AuditTrail {
  edited_by?: string;
  source_files?: string[];
  [key: string]: unknown;
}

export interface Meta {
  versioning: Versioning;
  creators?: Creator[];
  rights?: Rights;
  external_ids?: Record<string, string>;
  tags?: string[];
  audit?: AuditTrail;
  [key: string]: unknown;
}

export interface CharacterDefinition {
  kind: 'CharacterDefinition';
  ocs_version: string;
  $schema?: string;
  $id?: string;
  id: UUID;
  slug: Slug;
  names: Names;
  identity: Identity;
  appearance?: Record<string, unknown>;
  metaphysics?: Record<string, unknown>;
  personality?: Record<string, unknown>;
  background?: Record<string, unknown>;
  behavior?: Record<string, unknown>;
  media_profiles?: Record<string, unknown>;
  meta: Meta;
  extras?: Record<string, unknown>;
}

export interface Stat {
  key: string;
  value: number | string | boolean | Record<string, unknown> | Array<unknown>;
  unit?: string;
  min?: number;
  max?: number;
  temp?: boolean;
  [key: string]: unknown;
}

export interface EffectTimer {
  value: number;
  unit: string;
}

export interface ActiveEffect {
  effect: string;
  remaining?: EffectTimer;
  source_ref?: UUID;
  [key: string]: unknown;
}

export interface Cooldown {
  ability_ref: UUID;
  remaining: EffectTimer;
  [key: string]: unknown;
}

export interface InstanceState {
  stats?: Stat[];
  location_ref?: UUID;
  active_effects?: ActiveEffect[];
  cooldowns?: Cooldown[];
  [key: string]: unknown;
}

export interface CharacterInstance {
  kind: 'CharacterInstance';
  ocs_version: string;
  $schema?: string;
  $id?: string;
  instance_id: UUID;
  from_def: UUID;
  state: InstanceState;
  progression?: Record<string, unknown>;
  session?: Record<string, unknown>;
  extras?: Record<string, unknown>;
}

export type CoreDocument = CharacterDefinition | CharacterInstance;
