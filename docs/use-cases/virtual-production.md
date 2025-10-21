# Virtual Production


Integrate OCD characters into virtual production pipelines for real-time character management, cross-platform synchronization, and live production workflows.


OCD characters excel in virtual production environments where real-time character management and cross-platform compatibility are essential. This guide shows you how to build production-ready systems that enable live character updates, multi-platform synchronization, and seamless integration with production tools.

## Getting Started with Virtual Production

### Prerequisites

- Virtual production software (Unreal Engine, Unity, Blender, etc.)
- OCD character files in JSON format
- Real-time communication system (WebSocket, REST API)
- Understanding of production workflows

### Quick Setup

1. **Set Up Live Sync**: Implement real-time character updates
2. **Configure Multi-Platform**: Enable cross-platform character sharing
3. **Build Production Tools**: Create character management interfaces
4. **Test Continuity**: Ensure character consistency across productions

## Real-Time Character Management

### Virtual Production Character Manager

```python
class VirtualProductionCharacterManager:
    def __init__(self, ocd_api_client):
        self.api_client = ocd_api_client
        self.active_characters = {}
        self.character_versions = {}
        self.live_updates = True
        self.production_context = {}
        self.character_sync_queue = []
        self.production_tools = {}
    
    def load_character_for_production(self, character_id: str, scene_context: Dict[str, Any]):
        """Load character for virtual production with live updates"""
        # Fetch latest character data
        character_data = self.api_client.get_character(character_id)
        
        # Store character with version tracking
        self.active_characters[character_id] = character_data
        self.character_versions[character_id] = character_data.get("meta", {}).get("versioning", {}).get("last_modified")
        
        # Set up live updates
        if self.live_updates:
            self._setup_live_updates(character_id)
        
        # Configure character for scene
        self._configure_character_for_scene(character_id, scene_context)
        
        # Notify production systems
        self._notify_production_systems(character_id, character_data, "loaded")
    
    def _setup_live_updates(self, character_id: str):
        """Set up live updates for character data"""
        # Set up WebSocket connection for real-time updates
        self.api_client.subscribe_to_character_updates(
            character_id,
            callback=self._handle_character_update
        )
    
    def _handle_character_update(self, character_id: str, updated_data: Dict[str, Any]):
        """Handle real-time character updates"""
        if character_id in self.active_characters:
            # Update character data
            self.active_characters[character_id] = updated_data
            
            # Update version tracking
            self.character_versions[character_id] = updated_data.get("meta", {}).get("versioning", {}).get("last_modified")
            
            # Queue for sync
            self.character_sync_queue.append({
                "character_id": character_id,
                "action": "update",
                "data": updated_data,
                "timestamp": time.time()
            })
            
            # Notify production systems
            self._notify_production_systems(character_id, updated_data, "updated")
    
    def _configure_character_for_scene(self, character_id: str, scene_context: Dict[str, Any]):
        """Configure character for specific scene context"""
        character = self.active_characters[character_id]
        
        # Apply scene-specific modifications
        if scene_context.get("time_of_day") == "night":
            self._apply_night_modifications(character)
        
        if scene_context.get("mood") == "tense":
            self._apply_tense_modifications(character)
        
        if scene_context.get("weather") == "rain":
            self._apply_weather_modifications(character, "rain")
        
        # Update character in production system
        self._update_production_character(character_id, character)
    
    def _apply_night_modifications(self, character: Dict[str, Any]):
        """Apply night-time modifications to character"""
        # Modify character appearance for night scenes
        appearance = character.get("appearance", {})
        if "night_clothing" in appearance:
            appearance["clothing"] = appearance["night_clothing"]
        
        # Modify personality traits for night scenes
        personality = character.get("personality", {})
        for trait in personality.get("traits", []):
            if trait["name"] == "alertness":
                trait["value"] = min(1.0, trait["value"] + 0.2)
    
    def _apply_tense_modifications(self, character: Dict[str, Any]):
        """Apply tense scene modifications to character"""
        # Modify character behavior for tense scenes
        personality = character.get("personality", {})
        for trait in personality.get("traits", []):
            if trait["name"] == "stress-tolerance":
                trait["value"] = max(0.0, trait["value"] - 0.1)
    
    def _apply_weather_modifications(self, character: Dict[str, Any], weather: str):
        """Apply weather-specific modifications to character"""
        # Modify character appearance for weather
        appearance = character.get("appearance", {})
        if weather == "rain":
            if "rain_clothing" in appearance:
                appearance["clothing"] = appearance["rain_clothing"]
        
        # Modify personality traits for weather
        personality = character.get("personality", {})
        for trait in personality.get("traits", []):
            if trait["name"] == "mood":
                if weather == "rain":
                    trait["value"] = max(0.0, trait["value"] - 0.1)
                elif weather == "sunny":
                    trait["value"] = min(1.0, trait["value"] + 0.1)
    
    def _update_production_character(self, character_id: str, character_data: Dict[str, Any]):
        """Update character in production system"""
        # Update character in all active production tools
        for tool_name, tool in self.production_tools.items():
            if hasattr(tool, 'update_character'):
                tool.update_character(character_id, character_data)
    
    def _notify_production_systems(self, character_id: str, character_data: Dict[str, Any], action: str):
        """Notify all production systems of character changes"""
        notification = {
            "character_id": character_id,
            "action": action,
            "data": character_data,
            "timestamp": time.time()
        }
        
        # Send to all registered production tools
        for tool_name, tool in self.production_tools.items():
            if hasattr(tool, 'handle_character_notification'):
                tool.handle_character_notification(notification)
    
    def register_production_tool(self, tool_name: str, tool_instance):
        """Register a production tool for character updates"""
        self.production_tools[tool_name] = tool_instance
    
    def unregister_production_tool(self, tool_name: str):
        """Unregister a production tool"""
        if tool_name in self.production_tools:
            del self.production_tools[tool_name]
    
    def get_character_for_scene(self, character_id: str, scene_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get character data configured for specific scene"""
        if character_id not in self.active_characters:
            return None
        
        character = self.active_characters[character_id].copy()
        
        # Apply scene-specific modifications
        self._configure_character_for_scene(character_id, scene_context)
        
        return character
    
    def sync_character_changes(self, character_id: str, changes: Dict[str, Any]):
        """Sync character changes across all production systems"""
        if character_id not in self.active_characters:
            return False
        
        # Update local character data
        character = self.active_characters[character_id]
        self._apply_character_changes(character, changes)
        
        # Queue for sync
        self.character_sync_queue.append({
            "character_id": character_id,
            "action": "sync",
            "changes": changes,
            "timestamp": time.time()
        })
        
        # Notify production systems
        self._notify_production_systems(character_id, character, "synced")
        
        return True
    
    def _apply_character_changes(self, character: Dict[str, Any], changes: Dict[str, Any]):
        """Apply changes to character data"""
        for key, value in changes.items():
            if key in character:
                character[key] = value
            else:
                # Handle nested updates
                self._update_nested_value(character, key, value)
    
    def _update_nested_value(self, data: Dict[str, Any], key_path: str, value: Any):
        """Update nested value in character data"""
        keys = key_path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def get_character_version(self, character_id: str) -> str:
        """Get current version of character"""
        return self.character_versions.get(character_id, "unknown")
    
    def get_sync_queue(self) -> List[Dict[str, Any]]:
        """Get current sync queue"""
        return self.character_sync_queue.copy()
    
    def clear_sync_queue(self):
        """Clear the sync queue"""
        self.character_sync_queue.clear()
    
    def enable_live_updates(self):
        """Enable live updates for all characters"""
        self.live_updates = True
        for character_id in self.active_characters:
            self._setup_live_updates(character_id)
    
    def disable_live_updates(self):
        """Disable live updates for all characters"""
        self.live_updates = False
        # Disconnect WebSocket connections
        self.api_client.disconnect_all()
```

## Cross-Platform Character Sync

### Cross-Platform Synchronization System

```python
class CrossPlatformCharacterSync:
    def __init__(self, platforms: List[str]):
        self.platforms = platforms
        self.character_sync = {}
        self.sync_queues = {platform: [] for platform in platforms}
        self.platform_adapters = {}
        self.sync_conflicts = {}
        self.sync_history = []
    
    def sync_character_across_platforms(self, character_id: str, update_data: Dict[str, Any]):
        """Sync character updates across all platforms"""
        # Validate update data
        if not self._validate_update_data(update_data):
            return False
        
        # Check for conflicts
        conflicts = self._check_sync_conflicts(character_id, update_data)
        if conflicts:
            self._handle_sync_conflicts(character_id, update_data, conflicts)
            return False
        
        # Queue update for each platform
        for platform in self.platforms:
            self.sync_queues[platform].append({
                "character_id": character_id,
                "update_data": update_data,
                "timestamp": time.time(),
                "priority": self._calculate_priority(update_data)
            })
            
            # Process sync queue
            self._process_sync_queue(platform)
        
        # Record sync in history
        self.sync_history.append({
            "character_id": character_id,
            "update_data": update_data,
            "platforms": self.platforms.copy(),
            "timestamp": time.time()
        })
        
        return True
    
    def _validate_update_data(self, update_data: Dict[str, Any]) -> bool:
        """Validate update data before syncing"""
        required_fields = ["id", "version", "timestamp"]
        
        for field in required_fields:
            if field not in update_data:
                print(f"Missing required field: {field}")
                return False
        
        return True
    
    def _check_sync_conflicts(self, character_id: str, update_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for sync conflicts with other platforms"""
        conflicts = []
        
        # Check if character is being updated on multiple platforms
        for platform in self.platforms:
            if platform in self.character_sync:
                platform_data = self.character_sync[platform].get(character_id)
                if platform_data:
                    # Compare timestamps
                    if platform_data.get("timestamp", 0) > update_data.get("timestamp", 0):
                        conflicts.append({
                            "platform": platform,
                            "conflict_type": "timestamp",
                            "existing_data": platform_data,
                            "new_data": update_data
                        })
        
        return conflicts
    
    def _handle_sync_conflicts(self, character_id: str, update_data: Dict[str, Any], conflicts: List[Dict[str, Any]]):
        """Handle sync conflicts between platforms"""
        # Store conflict for manual resolution
        self.sync_conflicts[character_id] = {
            "conflicts": conflicts,
            "update_data": update_data,
            "timestamp": time.time()
        }
        
        # Notify conflict resolution system
        self._notify_conflict_resolution(character_id, conflicts)
    
    def _notify_conflict_resolution(self, character_id: str, conflicts: List[Dict[str, Any]]):
        """Notify conflict resolution system"""
        # This would integrate with a conflict resolution UI or system
        print(f"Sync conflict detected for character {character_id}: {conflicts}")
    
    def _calculate_priority(self, update_data: Dict[str, Any]) -> int:
        """Calculate priority for sync operation"""
        priority = 1  # Default priority
        
        # Increase priority for critical updates
        if update_data.get("critical", False):
            priority += 3
        
        # Increase priority for appearance changes
        if "appearance" in update_data:
            priority += 2
        
        # Increase priority for personality changes
        if "personality" in update_data:
            priority += 1
        
        return priority
    
    def _process_sync_queue(self, platform: str):
        """Process sync queue for specific platform"""
        queue = self.sync_queues[platform]
        
        # Sort by priority
        queue.sort(key=lambda x: x["priority"], reverse=True)
        
        while queue:
            sync_item = queue.pop(0)
            character_id = sync_item["character_id"]
            update_data = sync_item["update_data"]
            
            # Apply update to platform
            success = self._apply_update_to_platform(platform, character_id, update_data)
            
            if not success:
                # Re-queue failed update
                queue.insert(0, sync_item)
                break
    
    def _apply_update_to_platform(self, platform: str, character_id: str, update_data: Dict[str, Any]) -> bool:
        """Apply character update to specific platform"""
        try:
            if platform == "unity":
                return self._update_unity_character(character_id, update_data)
            elif platform == "unreal":
                return self._update_unreal_character(character_id, update_data)
            elif platform == "blender":
                return self._update_blender_character(character_id, update_data)
            elif platform == "maya":
                return self._update_maya_character(character_id, update_data)
            else:
                return False
        except Exception as e:
            print(f"Failed to update {platform} character {character_id}: {e}")
            return False
    
    def _update_unity_character(self, character_id: str, update_data: Dict[str, Any]) -> bool:
        """Update character in Unity"""
        # Unity-specific update logic
        try:
            # Send update to Unity via API or file system
            unity_api = self.platform_adapters.get("unity")
            if unity_api:
                return unity_api.update_character(character_id, update_data)
            else:
                # Fallback to file-based update
                return self._update_character_file(character_id, update_data, "unity")
        except Exception as e:
            print(f"Unity update failed: {e}")
            return False
    
    def _update_unreal_character(self, character_id: str, update_data: Dict[str, Any]) -> bool:
        """Update character in Unreal Engine"""
        # Unreal-specific update logic
        try:
            unreal_api = self.platform_adapters.get("unreal")
            if unreal_api:
                return unreal_api.update_character(character_id, update_data)
            else:
                return self._update_character_file(character_id, update_data, "unreal")
        except Exception as e:
            print(f"Unreal update failed: {e}")
            return False
    
    def _update_blender_character(self, character_id: str, update_data: Dict[str, Any]) -> bool:
        """Update character in Blender"""
        # Blender-specific update logic
        try:
            blender_api = self.platform_adapters.get("blender")
            if blender_api:
                return blender_api.update_character(character_id, update_data)
            else:
                return self._update_character_file(character_id, update_data, "blender")
        except Exception as e:
            print(f"Blender update failed: {e}")
            return False
    
    def _update_maya_character(self, character_id: str, update_data: Dict[str, Any]) -> bool:
        """Update character in Maya"""
        # Maya-specific update logic
        try:
            maya_api = self.platform_adapters.get("maya")
            if maya_api:
                return maya_api.update_character(character_id, update_data)
            else:
                return self._update_character_file(character_id, update_data, "maya")
        except Exception as e:
            print(f"Maya update failed: {e}")
            return False
    
    def _update_character_file(self, character_id: str, update_data: Dict[str, Any], platform: str) -> bool:
        """Update character file for platform"""
        try:
            # Create platform-specific file path
            file_path = f"characters/{platform}/{character_id}.json"
            
            # Load existing character data
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    character_data = json.load(f)
            else:
                character_data = {}
            
            # Apply updates
            character_data.update(update_data)
            
            # Save updated character data
            with open(file_path, 'w') as f:
                json.dump(character_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"File update failed for {platform}: {e}")
            return False
    
    def register_platform_adapter(self, platform: str, adapter):
        """Register platform adapter for direct API communication"""
        self.platform_adapters[platform] = adapter
    
    def get_sync_status(self, character_id: str) -> Dict[str, Any]:
        """Get sync status for character across platforms"""
        status = {
            "character_id": character_id,
            "platforms": {},
            "last_sync": None,
            "conflicts": []
        }
        
        # Check each platform
        for platform in self.platforms:
            platform_data = self.character_sync.get(platform, {}).get(character_id)
            if platform_data:
                status["platforms"][platform] = {
                    "synced": True,
                    "timestamp": platform_data.get("timestamp"),
                    "version": platform_data.get("version")
                }
            else:
                status["platforms"][platform] = {
                    "synced": False,
                    "timestamp": None,
                    "version": None
                }
        
        # Check for conflicts
        if character_id in self.sync_conflicts:
            status["conflicts"] = self.sync_conflicts[character_id]["conflicts"]
        
        # Get last sync time
        sync_history = [h for h in self.sync_history if h["character_id"] == character_id]
        if sync_history:
            status["last_sync"] = max(h["timestamp"] for h in sync_history)
        
        return status
    
    def resolve_sync_conflict(self, character_id: str, resolution: Dict[str, Any]):
        """Resolve sync conflict for character"""
        if character_id in self.sync_conflicts:
            # Apply resolution
            resolved_data = self.sync_conflicts[character_id]["update_data"]
            resolved_data.update(resolution)
            
            # Clear conflict
            del self.sync_conflicts[character_id]
            
            # Re-sync with resolved data
            return self.sync_character_across_platforms(character_id, resolved_data)
        
        return False
```

## Production Tools Integration

### Production Tools Manager

```python
class ProductionToolsManager:
    def __init__(self):
        self.tools = {}
        self.tool_connections = {}
        self.production_pipeline = []
        self.quality_checks = []
    
    def register_tool(self, tool_name: str, tool_instance):
        """Register a production tool"""
        self.tools[tool_name] = tool_instance
        
        # Set up tool connections
        self._setup_tool_connections(tool_name, tool_instance)
    
    def _setup_tool_connections(self, tool_name: str, tool_instance):
        """Set up connections between tools"""
        # Connect tool to character update system
        if hasattr(tool_instance, 'handle_character_update'):
            self.tool_connections[tool_name] = {
                'character_updates': tool_instance.handle_character_update,
                'scene_changes': getattr(tool_instance, 'handle_scene_change', None),
                'production_events': getattr(tool_instance, 'handle_production_event', None)
            }
    
    def handle_character_update(self, character_id: str, update_data: Dict[str, Any]):
        """Handle character update across all tools"""
        for tool_name, connections in self.tool_connections.items():
            if connections['character_updates']:
                try:
                    connections['character_updates'](character_id, update_data)
                except Exception as e:
                    print(f"Error updating {tool_name}: {e}")
    
    def handle_scene_change(self, scene_data: Dict[str, Any]):
        """Handle scene change across all tools"""
        for tool_name, connections in self.tool_connections.items():
            if connections['scene_changes']:
                try:
                    connections['scene_changes'](scene_data)
                except Exception as e:
                    print(f"Error updating {tool_name} scene: {e}")
    
    def handle_production_event(self, event_data: Dict[str, Any]):
        """Handle production event across all tools"""
        for tool_name, connections in self.tool_connections.items():
            if connections['production_events']:
                try:
                    connections['production_events'](event_data)
                except Exception as e:
                    print(f"Error handling {tool_name} event: {e}")
    
    def add_quality_check(self, check_function):
        """Add quality check to production pipeline"""
        self.quality_checks.append(check_function)
    
    def run_quality_checks(self, character_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Run quality checks on character data"""
        issues = []
        
        for check in self.quality_checks:
            try:
                result = check(character_data)
                if result:
                    issues.extend(result)
            except Exception as e:
                print(f"Quality check failed: {e}")
        
        return issues
    
    def get_production_status(self) -> Dict[str, Any]:
        """Get current production status"""
        status = {
            "tools": {},
            "pipeline": self.production_pipeline.copy(),
            "quality_issues": []
        }
        
        # Check tool status
        for tool_name, tool in self.tools.items():
            status["tools"][tool_name] = {
                "connected": tool_name in self.tool_connections,
                "status": getattr(tool, 'get_status', lambda: "unknown")(),
                "last_update": getattr(tool, 'last_update', None)
            }
        
        return status
```

## Live Production Workflow

### Live Production Controller

```python
class LiveProductionController:
    def __init__(self, character_manager, sync_system, tools_manager):
        self.character_manager = character_manager
        self.sync_system = sync_system
        self.tools_manager = tools_manager
        self.production_state = "idle"
        self.active_scene = None
        self.live_characters = []
        self.production_log = []
    
    def start_production(self, scene_data: Dict[str, Any]):
        """Start live production session"""
        self.production_state = "active"
        self.active_scene = scene_data
        
        # Load characters for scene
        for character_id in scene_data.get("characters", []):
            self.load_character_for_live(character_id, scene_data)
        
        # Notify all tools
        self.tools_manager.handle_scene_change(scene_data)
        
        # Log production start
        self._log_production_event("production_started", scene_data)
    
    def load_character_for_live(self, character_id: str, scene_data: Dict[str, Any]):
        """Load character for live production"""
        # Load character with live updates
        self.character_manager.load_character_for_production(character_id, scene_data)
        
        # Add to live characters list
        if character_id not in self.live_characters:
            self.live_characters.append(character_id)
        
        # Set up real-time sync
        self.sync_system.sync_character_across_platforms(character_id, {
            "live_production": True,
            "scene": scene_data.get("scene_id"),
            "timestamp": time.time()
        })
    
    def update_character_live(self, character_id: str, changes: Dict[str, Any]):
        """Update character during live production"""
        if character_id not in self.live_characters:
            return False
        
        # Apply changes
        success = self.character_manager.sync_character_changes(character_id, changes)
        
        if success:
            # Sync across platforms
            self.sync_system.sync_character_across_platforms(character_id, changes)
            
            # Log update
            self._log_production_event("character_updated", {
                "character_id": character_id,
                "changes": changes
            })
        
        return success
    
    def end_production(self):
        """End live production session"""
        self.production_state = "idle"
        
        # Unload live characters
        for character_id in self.live_characters:
            self._unload_character_from_live(character_id)
        
        # Clear live characters list
        self.live_characters.clear()
        
        # Log production end
        self._log_production_event("production_ended", {
            "scene": self.active_scene,
            "duration": time.time() - self.production_log[0]["timestamp"] if self.production_log else 0
        })
        
        self.active_scene = None
    
    def _unload_character_from_live(self, character_id: str):
        """Unload character from live production"""
        # Remove from live characters
        if character_id in self.live_characters:
            self.live_characters.remove(character_id)
        
        # Disable live updates
        # This would be implemented based on the character manager's capabilities
    
    def _log_production_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log production event"""
        event = {
            "type": event_type,
            "data": event_data,
            "timestamp": time.time()
        }
        
        self.production_log.append(event)
        
        # Notify tools of production event
        self.tools_manager.handle_production_event(event)
    
    def get_production_status(self) -> Dict[str, Any]:
        """Get current production status"""
        return {
            "state": self.production_state,
            "active_scene": self.active_scene,
            "live_characters": self.live_characters.copy(),
            "tools_status": self.tools_manager.get_production_status(),
            "sync_status": self._get_sync_status()
        }
    
    def _get_sync_status(self) -> Dict[str, Any]:
        """Get sync status for all live characters"""
        sync_status = {}
        
        for character_id in self.live_characters:
            sync_status[character_id] = self.sync_system.get_sync_status(character_id)
        
        return sync_status
    
    def get_production_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get production log"""
        return self.production_log[-limit:] if limit else self.production_log
```

## Best Practices

### Performance Optimization

1. **Efficient Sync**: Use efficient synchronization algorithms
2. **Caching**: Cache frequently accessed character data
3. **Batch Updates**: Batch multiple updates together
4. **Lazy Loading**: Load character data only when needed

### Production Quality

1. **Version Control**: Maintain character version history
2. **Conflict Resolution**: Implement robust conflict resolution
3. **Quality Checks**: Run quality checks on character data
4. **Backup Systems**: Maintain backup systems for production data

### Real-Time Management

1. **Live Updates**: Ensure real-time updates work reliably
2. **Error Handling**: Implement robust error handling
3. **Monitoring**: Monitor production systems continuously
4. **Recovery**: Implement recovery mechanisms for failures

### Cross-Platform Compatibility

1. **Platform Adapters**: Use platform-specific adapters
2. **Data Validation**: Validate data across platforms
3. **Format Conversion**: Convert data formats as needed
4. **Testing**: Test across all target platforms

!!! tip "Ready for Virtual Production?"
    Check out our [Python Validator](../integration/python-validator.md) to validate your OCD files before importing, or explore our [Examples Gallery](../authoring/examples.md) for character inspiration.
