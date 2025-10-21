# Unreal Engine Integration


Integrate OCD characters into Unreal Engine projects using Blueprint-friendly C++ classes and Blueprint visual scripting for maximum flexibility and performance.


Unreal Engine's powerful C++ foundation and Blueprint system make it ideal for creating sophisticated character systems. This guide shows you how to build a complete OCD character integration system that works seamlessly with Unreal's architecture.

## Getting Started with Unreal Engine

### Prerequisites

- Unreal Engine 5.3 or newer
- Visual Studio 2022 or Visual Studio Code
- Basic understanding of C++ and Blueprint scripting
- OCD character files in JSON format

### Quick Setup

1. **Create C++ Classes**: Set up the core OCD integration classes
2. **Create Blueprint Classes**: Build Blueprint-friendly wrappers
3. **Set Up Data Assets**: Create OCD character data assets
4. **Test Integration**: Import and test your first character

## Core C++ Classes

### OCD Data Structures

```cpp
// OCDCharacterData.h
#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "OCDCharacterData.generated.h"

USTRUCT(BlueprintType)
struct FOCDTrait
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Trait")
    FString Name;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Trait")
    FString Kind;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Trait")
    float Value;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Trait")
    float Polarity;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Trait")
    float Intensity;

    FOCDTrait()
    {
        Name = TEXT("");
        Kind = TEXT("");
        Value = 0.0f;
        Polarity = 0.0f;
        Intensity = 0.0f;
    }
};

USTRUCT(BlueprintType)
struct FOCDNames
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Names")
    FString Canon;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Names")
    TArray<FString> Aliases;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Names")
    TArray<FString> Nicknames;

    FOCDNames()
    {
        Canon = TEXT("");
        Aliases.Empty();
        Nicknames.Empty();
    }
};

USTRUCT(BlueprintType)
struct FOCDIdentity
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Identity")
    FString Species;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Identity")
    int32 Age;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Identity")
    FString Gender;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Identity")
    TArray<FString> Roles;

    FOCDIdentity()
    {
        Species = TEXT("");
        Age = 0;
        Gender = TEXT("");
        Roles.Empty();
    }
};

USTRUCT(BlueprintType)
struct FOCDPersonality
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Personality")
    TArray<FOCDTrait> Traits;

    FOCDPersonality()
    {
        Traits.Empty();
    }
};

USTRUCT(BlueprintType)
struct FOCDAppearance
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Appearance")
    TArray<FString> PhysicalDescription;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Appearance")
    TArray<FString> Clothing;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Appearance")
    TArray<FString> Accessories;

    FOCDAppearance()
    {
        PhysicalDescription.Empty();
        Clothing.Empty();
        Accessories.Empty();
    }
};

USTRUCT(BlueprintType)
struct FOCDCharacter
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Character")
    FString ID;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Character")
    FOCDNames Names;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Character")
    FOCDIdentity Identity;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Character")
    FOCDPersonality Personality;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Character")
    FOCDAppearance Appearance;

    FOCDCharacter()
    {
        ID = TEXT("");
    }
};

UCLASS(BlueprintType, Blueprintable)
class MYGAME_API UOCDCharacterData : public UDataAsset
{
    GENERATED_BODY()

public:
    UOCDCharacterData();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OCD Character")
    FOCDCharacter CharacterData;

    UFUNCTION(BlueprintCallable, Category = "OCD Character")
    FString GetCharacterName() const;

    UFUNCTION(BlueprintCallable, Category = "OCD Character")
    float GetTraitValue(const FString& TraitName) const;

    UFUNCTION(BlueprintCallable, Category = "OCD Character")
    float GetTraitPolarity(const FString& TraitName) const;

    UFUNCTION(BlueprintCallable, Category = "OCD Character")
    bool HasTrait(const FString& TraitName) const;
};
```

### OCD Character Importer

```cpp
// OCDCharacterImporter.h
#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "OCDCharacterData.h"
#include "OCDCharacterImporter.generated.h"

UCLASS(BlueprintType, Blueprintable)
class MYGAME_API UOCDCharacterImporter : public UObject
{
    GENERATED_BODY()

public:
    UOCDCharacterImporter();

    UFUNCTION(BlueprintCallable, Category = "OCD Import")
    static UOCDCharacterData* ImportFromJSON(const FString& JSONPath);

    UFUNCTION(BlueprintCallable, Category = "OCD Import")
    static bool ImportFromJSONString(const FString& JSONString, FOCDCharacter& OutCharacter);

    UFUNCTION(BlueprintCallable, Category = "OCD Import")
    static void ApplyToActor(AActor* TargetActor, const FOCDCharacter& CharacterData);

    UFUNCTION(BlueprintCallable, Category = "OCD Import")
    static float GetTraitValue(const FOCDCharacter& Character, const FString& TraitName);

    UFUNCTION(BlueprintCallable, Category = "OCD Import")
    static float GetTraitPolarity(const FOCDCharacter& Character, const FString& TraitName);

private:
    static bool ParseJSONString(const FString& JSONString, FOCDCharacter& OutCharacter);
    static void ApplyPersonalityTraits(AActor* TargetActor, const TArray<FOCDTrait>& Traits);
    static void ApplyAppearance(AActor* TargetActor, const FOCDAppearance& Appearance);
    static void SetupAIBehavior(AActor* TargetActor, const TArray<FOCDTrait>& Traits);
};
```

```cpp
// OCDCharacterImporter.cpp
#include "OCDCharacterImporter.h"
#include "OCDCharacterData.h"
#include "Engine/DataAsset.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonReader.h"
#include "Misc/FileHelper.h"
#include "HAL/PlatformFilemanager.h"

UOCDCharacterImporter::UOCDCharacterImporter()
{
}

UOCDCharacterData* UOCDCharacterImporter::ImportFromJSON(const FString& JSONPath)
{
    FString JSONString;
    if (!FFileHelper::LoadFileToString(JSONString, *JSONPath))
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to load JSON file: %s"), *JSONPath);
        return nullptr;
    }

    FOCDCharacter CharacterData;
    if (!ImportFromJSONString(JSONString, CharacterData))
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to parse JSON file: %s"), *JSONPath);
        return nullptr;
    }

    // Create data asset
    UOCDCharacterData* CharacterDataAsset = NewObject<UOCDCharacterData>();
    CharacterDataAsset->CharacterData = CharacterData;
    
    return CharacterDataAsset;
}

bool UOCDCharacterImporter::ImportFromJSONString(const FString& JSONString, FOCDCharacter& OutCharacter)
{
    return ParseJSONString(JSONString, OutCharacter);
}

void UOCDCharacterImporter::ApplyToActor(AActor* TargetActor, const FOCDCharacter& CharacterData)
{
    if (!TargetActor)
    {
        UE_LOG(LogTemp, Error, TEXT("Target actor is null"));
        return;
    }

    // Apply personality traits
    ApplyPersonalityTraits(TargetActor, CharacterData.Personality.Traits);
    
    // Apply appearance
    ApplyAppearance(TargetActor, CharacterData.Appearance);
    
    // Setup AI behavior
    SetupAIBehavior(TargetActor, CharacterData.Personality.Traits);
}

float UOCDCharacterImporter::GetTraitValue(const FOCDCharacter& Character, const FString& TraitName)
{
    for (const FOCDTrait& Trait : Character.Personality.Traits)
    {
        if (Trait.Name == TraitName)
        {
            return Trait.Value;
        }
    }
    return 0.0f;
}

float UOCDCharacterImporter::GetTraitPolarity(const FOCDCharacter& Character, const FString& TraitName)
{
    for (const FOCDTrait& Trait : Character.Personality.Traits)
    {
        if (Trait.Name == TraitName)
        {
            return Trait.Polarity;
        }
    }
    return 0.0f;
}

bool UOCDCharacterImporter::ParseJSONString(const FString& JSONString, FOCDCharacter& OutCharacter)
{
    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JSONString);
    
    if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to parse JSON string"));
        return false;
    }

    // Parse basic character info
    OutCharacter.ID = JsonObject->GetStringField(TEXT("id"));
    
    // Parse names
    TSharedPtr<FJsonObject> NamesObject = JsonObject->GetObjectField(TEXT("names"));
    if (NamesObject.IsValid())
    {
        OutCharacter.Names.Canon = NamesObject->GetStringField(TEXT("canon"));
        
        const TArray<TSharedPtr<FJsonValue>>* AliasesArray;
        if (NamesObject->TryGetArrayField(TEXT("aliases"), AliasesArray))
        {
            for (const TSharedPtr<FJsonValue>& AliasValue : *AliasesArray)
            {
                OutCharacter.Names.Aliases.Add(AliasValue->AsString());
            }
        }
    }
    
    // Parse identity
    TSharedPtr<FJsonObject> IdentityObject = JsonObject->GetObjectField(TEXT("identity"));
    if (IdentityObject.IsValid())
    {
        OutCharacter.Identity.Species = IdentityObject->GetStringField(TEXT("species"));
        OutCharacter.Identity.Age = IdentityObject->GetIntegerField(TEXT("age"));
        OutCharacter.Identity.Gender = IdentityObject->GetStringField(TEXT("gender"));
        
        const TArray<TSharedPtr<FJsonValue>>* RolesArray;
        if (IdentityObject->TryGetArrayField(TEXT("roles"), RolesArray))
        {
            for (const TSharedPtr<FJsonValue>& RoleValue : *RolesArray)
            {
                OutCharacter.Identity.Roles.Add(RoleValue->AsString());
            }
        }
    }
    
    // Parse personality traits
    TSharedPtr<FJsonObject> PersonalityObject = JsonObject->GetObjectField(TEXT("personality"));
    if (PersonalityObject.IsValid())
    {
        const TArray<TSharedPtr<FJsonValue>>* TraitsArray;
        if (PersonalityObject->TryGetArrayField(TEXT("traits"), TraitsArray))
        {
            for (const TSharedPtr<FJsonValue>& TraitValue : *TraitsArray)
            {
                TSharedPtr<FJsonObject> TraitObject = TraitValue->AsObject();
                if (TraitObject.IsValid())
                {
                    FOCDTrait Trait;
                    Trait.Name = TraitObject->GetStringField(TEXT("name"));
                    Trait.Kind = TraitObject->GetStringField(TEXT("kind"));
                    Trait.Value = TraitObject->GetNumberField(TEXT("value"));
                    Trait.Polarity = TraitObject->GetNumberField(TEXT("polarity"));
                    Trait.Intensity = TraitObject->GetNumberField(TEXT("intensity"));
                    
                    OutCharacter.Personality.Traits.Add(Trait);
                }
            }
        }
    }
    
    // Parse appearance
    TSharedPtr<FJsonObject> AppearanceObject = JsonObject->GetObjectField(TEXT("appearance"));
    if (AppearanceObject.IsValid())
    {
        const TArray<TSharedPtr<FJsonValue>>* PhysicalArray;
        if (AppearanceObject->TryGetArrayField(TEXT("physical_description"), PhysicalArray))
        {
            for (const TSharedPtr<FJsonValue>& PhysicalValue : *PhysicalArray)
            {
                OutCharacter.Appearance.PhysicalDescription.Add(PhysicalValue->AsString());
            }
        }
        
        const TArray<TSharedPtr<FJsonValue>>* ClothingArray;
        if (AppearanceObject->TryGetArrayField(TEXT("clothing"), ClothingArray))
        {
            for (const TSharedPtr<FJsonValue>& ClothingValue : *ClothingArray)
            {
                OutCharacter.Appearance.Clothing.Add(ClothingValue->AsString());
            }
        }
    }
    
    return true;
}

void UOCDCharacterImporter::ApplyPersonalityTraits(AActor* TargetActor, const TArray<FOCDTrait>& Traits)
{
    // Find or create personality component
    UOCDPersonalityComponent* PersonalityComp = TargetActor->FindComponentByClass<UOCDPersonalityComponent>();
    if (!PersonalityComp)
    {
        PersonalityComp = NewObject<UOCDPersonalityComponent>(TargetActor);
        TargetActor->AddInstanceComponent(PersonalityComp);
    }
    
    // Apply traits
    for (const FOCDTrait& Trait : Traits)
    {
        if (Trait.Name == TEXT("introversion-extraversion"))
        {
            PersonalityComp->SetExtraversion(Trait.Polarity);
        }
        else if (Trait.Name == TEXT("combat-readiness"))
        {
            PersonalityComp->SetCombatReadiness(Trait.Value);
        }
        else if (Trait.Name == TEXT("moral-uprightness"))
        {
            PersonalityComp->SetMoralAlignment(Trait.Value);
        }
        // Add more trait mappings as needed
    }
}

void UOCDCharacterImporter::ApplyAppearance(AActor* TargetActor, const FOCDAppearance& Appearance)
{
    // Find or create appearance component
    UOCDAppearanceComponent* AppearanceComp = TargetActor->FindComponentByClass<UOCDAppearanceComponent>();
    if (!AppearanceComp)
    {
        AppearanceComp = NewObject<UOCDAppearanceComponent>(TargetActor);
        TargetActor->AddInstanceComponent(AppearanceComp);
    }
    
    // Apply appearance data
    AppearanceComp->SetPhysicalDescription(Appearance.PhysicalDescription);
    AppearanceComp->SetClothing(Appearance.Clothing);
    AppearanceComp->SetAccessories(Appearance.Accessories);
}

void UOCDCharacterImporter::SetupAIBehavior(AActor* TargetActor, const TArray<FOCDTrait>& Traits)
{
    // Find or create AI behavior component
    UOCDBehaviorComponent* BehaviorComp = TargetActor->FindComponentByClass<UOCDBehaviorComponent>();
    if (!BehaviorComp)
    {
        BehaviorComp = NewObject<UOCDBehaviorComponent>(TargetActor);
        TargetActor->AddInstanceComponent(BehaviorComp);
    }
    
    // Configure behavior based on traits
    for (const FOCDTrait& Trait : Traits)
    {
        if (Trait.Name == TEXT("introversion-extraversion"))
        {
            if (Trait.Polarity > 0.3f)
            {
                BehaviorComp->SetSocialBehavior(ESocialBehavior::Extroverted);
            }
            else if (Trait.Polarity < -0.3f)
            {
                BehaviorComp->SetSocialBehavior(ESocialBehavior::Introverted);
            }
            else
            {
                BehaviorComp->SetSocialBehavior(ESocialBehavior::Balanced);
            }
        }
        else if (Trait.Name == TEXT("combat-readiness"))
        {
            if (Trait.Value > 0.7f)
            {
                BehaviorComp->SetCombatBehavior(ECombatBehavior::Aggressive);
            }
            else if (Trait.Value < 0.3f)
            {
                BehaviorComp->SetCombatBehavior(ECombatBehavior::Defensive);
            }
            else
            {
                BehaviorComp->SetCombatBehavior(ECombatBehavior::Balanced);
            }
        }
    }
}
```

## Behavior Component System

### OCD Behavior Component

```cpp
// OCDBehaviorComponent.h
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "OCDBehaviorComponent.generated.h"

UENUM(BlueprintType)
enum class ESocialBehavior : uint8
{
    Introverted,
    Balanced,
    Extroverted
};

UENUM(BlueprintType)
enum class ECombatBehavior : uint8
{
    Defensive,
    Balanced,
    Aggressive
};

UENUM(BlueprintType)
enum class EMoralBehavior : uint8
{
    Villainous,
    Neutral,
    Heroic
};

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class MYGAME_API UOCDBehaviorComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UOCDBehaviorComponent();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Behavior Settings")
    ESocialBehavior SocialBehavior = ESocialBehavior::Balanced;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Behavior Settings")
    ECombatBehavior CombatBehavior = ECombatBehavior::Balanced;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Behavior Settings")
    EMoralBehavior MoralBehavior = EMoralBehavior::Neutral;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI Components")
    class UBehaviorTreeComponent* BehaviorTreeComponent;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI Components")
    class UBlackboardComponent* BlackboardComponent;

    UFUNCTION(BlueprintCallable, Category = "OCD Behavior")
    void SetSocialBehavior(ESocialBehavior NewBehavior);
    
    UFUNCTION(BlueprintCallable, Category = "OCD Behavior")
    void SetCombatBehavior(ECombatBehavior NewBehavior);
    
    UFUNCTION(BlueprintCallable, Category = "OCD Behavior")
    void SetMoralBehavior(EMoralBehavior NewBehavior);

    UFUNCTION(BlueprintCallable, Category = "OCD Behavior")
    ESocialBehavior GetSocialBehavior() const { return SocialBehavior; }
    
    UFUNCTION(BlueprintCallable, Category = "OCD Behavior")
    ECombatBehavior GetCombatBehavior() const { return CombatBehavior; }
    
    UFUNCTION(BlueprintCallable, Category = "OCD Behavior")
    EMoralBehavior GetMoralBehavior() const { return MoralBehavior; }

private:
    void UpdateBehaviorTree();
    void UpdateBlackboardValues();
};
```

```cpp
// OCDBehaviorComponent.cpp
#include "OCDBehaviorComponent.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "AIController.h"

UOCDBehaviorComponent::UOCDBehaviorComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    SocialBehavior = ESocialBehavior::Balanced;
    CombatBehavior = ECombatBehavior::Balanced;
    MoralBehavior = EMoralBehavior::Neutral;
}

void UOCDBehaviorComponent::BeginPlay()
{
    Super::BeginPlay();
    
    // Find AI components
    AAIController* AIController = Cast<AAIController>(GetOwner()->GetInstigatorController());
    if (AIController)
    {
        BehaviorTreeComponent = AIController->FindComponentByClass<UBehaviorTreeComponent>();
        BlackboardComponent = AIController->FindComponentByClass<UBlackboardComponent>();
    }
    
    UpdateBehaviorTree();
}

void UOCDBehaviorComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
}

void UOCDBehaviorComponent::SetSocialBehavior(ESocialBehavior NewBehavior)
{
    SocialBehavior = NewBehavior;
    UpdateBehaviorTree();
}

void UOCDBehaviorComponent::SetCombatBehavior(ECombatBehavior NewBehavior)
{
    CombatBehavior = NewBehavior;
    UpdateBehaviorTree();
}

void UOCDBehaviorComponent::SetMoralBehavior(EMoralBehavior NewBehavior)
{
    MoralBehavior = NewBehavior;
    UpdateBehaviorTree();
}

void UOCDBehaviorComponent::UpdateBehaviorTree()
{
    UpdateBlackboardValues();
    
    if (BehaviorTreeComponent)
    {
        BehaviorTreeComponent->RestartTree();
    }
}

void UOCDBehaviorComponent::UpdateBlackboardValues()
{
    if (BlackboardComponent)
    {
        BlackboardComponent->SetValueAsEnum(TEXT("SocialBehavior"), (uint8)SocialBehavior);
        BlackboardComponent->SetValueAsEnum(TEXT("CombatBehavior"), (uint8)CombatBehavior);
        BlackboardComponent->SetValueAsEnum(TEXT("MoralBehavior"), (uint8)MoralBehavior);
    }
}
```

## Blueprint Integration

### Blueprint-Friendly Functions

```cpp
// OCDBlueprintLibrary.h
#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "OCDCharacterData.h"
#include "OCDBlueprintLibrary.generated.h"

UCLASS()
class MYGAME_API UOCDBlueprintLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "OCD", CallInEditor = true)
    static UOCDCharacterData* ImportCharacterFromFile(const FString& FilePath);
    
    UFUNCTION(BlueprintCallable, Category = "OCD")
    static void ApplyCharacterToActor(AActor* TargetActor, UOCDCharacterData* CharacterData);
    
    UFUNCTION(BlueprintCallable, Category = "OCD")
    static float GetCharacterTraitValue(UOCDCharacterData* CharacterData, const FString& TraitName);
    
    UFUNCTION(BlueprintCallable, Category = "OCD")
    static float GetCharacterTraitPolarity(UOCDCharacterData* CharacterData, const FString& TraitName);
    
    UFUNCTION(BlueprintCallable, Category = "OCD")
    static bool CharacterHasTrait(UOCDCharacterData* CharacterData, const FString& TraitName);
    
    UFUNCTION(BlueprintCallable, Category = "OCD")
    static FString GetCharacterName(UOCDCharacterData* CharacterData);
    
    UFUNCTION(BlueprintCallable, Category = "OCD")
    static FString GetCharacterSpecies(UOCDCharacterData* CharacterData);
    
    UFUNCTION(BlueprintCallable, Category = "OCD")
    static int32 GetCharacterAge(UOCDCharacterData* CharacterData);
};
```

### Blueprint Usage Examples

**Import Character in Blueprint:**
1. Create a Blueprint that inherits from Actor
2. Add a custom event called "Import Character"
3. Use the "Import Character From File" function
4. Store the result in a variable of type "OCD Character Data"

**Apply Character to Actor:**
1. Get a reference to your target actor
2. Use the "Apply Character to Actor" function
3. Pass the actor and character data as parameters

**Access Character Traits:**
1. Use "Get Character Trait Value" or "Get Character Trait Polarity"
2. Specify the trait name (e.g., "introversion-extraversion")
3. Use the returned float value in your logic

## Advanced Features

### Custom Trait Handlers

```cpp
// OCDTraitHandler.h
#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "OCDTraitHandler.generated.h"

UCLASS(BlueprintType, Blueprintable)
class MYGAME_API UOCDTraitHandler : public UObject
{
    GENERATED_BODY()

public:
    UOCDTraitHandler();

    UFUNCTION(BlueprintImplementableEvent, Category = "OCD Trait")
    void OnTraitChanged(const FString& TraitName, float NewValue, float NewPolarity);
    
    UFUNCTION(BlueprintCallable, Category = "OCD Trait")
    virtual void HandleTrait(const FString& TraitName, float Value, float Polarity);
    
    UFUNCTION(BlueprintCallable, Category = "OCD Trait")
    virtual bool CanHandleTrait(const FString& TraitName) const;
};
```

### Performance Optimization

```cpp
// OCDPerformanceOptimizer.h
#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "OCDPerformanceOptimizer.generated.h"

UCLASS(BlueprintType, Blueprintable)
class MYGAME_API UOCDPerformanceOptimizer : public UObject
{
    GENERATED_BODY()

public:
    UOCDPerformanceOptimizer();

    UFUNCTION(BlueprintCallable, Category = "OCD Performance")
    static void OptimizeCharacterData(UOCDCharacterData* CharacterData);
    
    UFUNCTION(BlueprintCallable, Category = "OCD Performance")
    static void CacheTraitValues(UOCDCharacterData* CharacterData);
    
    UFUNCTION(BlueprintCallable, Category = "OCD Performance")
    static void PreloadCharacterAssets(UOCDCharacterData* CharacterData);
};
```

## Best Practices

### Memory Management

1. **Use Data Assets**: Store character data in Data Assets for better memory management
2. **Object Pooling**: Implement object pooling for frequently spawned characters
3. **Lazy Loading**: Load character data only when needed
4. **Garbage Collection**: Properly manage object references to avoid memory leaks

### Performance Tips

1. **Batch Updates**: Update multiple characters in batches
2. **LOD System**: Use Level of Detail for distant characters
3. **Caching**: Cache frequently accessed trait values
4. **Async Loading**: Load character data asynchronously

### Blueprint Best Practices

1. **Use Functions**: Create reusable Blueprint functions for common operations
2. **Event-Driven**: Use events for character state changes
3. **Modular Design**: Keep character systems modular and reusable
4. **Documentation**: Add comments and documentation to Blueprint nodes

!!! tip "Ready to Integrate?"
    Check out our [Python Validator](../integration/python-validator.md) to validate your OCD files before importing, or explore our [Examples Gallery](../authoring/examples.md) for character inspiration.
