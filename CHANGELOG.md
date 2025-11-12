# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[English](CHANGELOG.md) | [한국어](CHANGELOG.ko.md)

## [1.2.0] - 2025-01-12

### Added
- 🆕 **GPT-5 Prompt Optimization Support**
  - GPT-5 prompting guide-based professional optimization engine
  - `gpt5_analyzer.py`: GPT-5 specialized analyzer
    - Contradiction detection (GPT-5 is highly sensitive to contradictions)
    - Agentic structure evaluation (tool usage, persistence, escape hatches)
    - Automatic parameter recommendations (reasoning_effort, verbosity)
    - Tool preamble quality assessment
    - Context efficiency analysis
  - `gpt5_optimizer.py`: GPT-5 optimizer
    - Automatic contradiction removal and integration
    - XML structuring (hierarchical prompts)
    - Automatic tool preamble insertion
    - Agentic pattern application (eagerness control)
    - Anti-pattern auto-fix
  - `gpt5_core.py`: Unified engine
    - Analysis + optimization pipeline
    - Convenient API functions
  - `gpt5_patterns.json`: GPT-5 pattern library
    - Agentic patterns (low/medium/high eagerness)
    - XML templates (basic, agentic, code_editing)
    - Contradiction pattern dictionary
    - Anti-pattern definitions and fix strategies
- **New Slash Commands**
  - `/analyze-gpt5-prompt`: GPT-5 specialized analysis
  - `/optimize-gpt5-prompt`: GPT-5 optimization (--include-analysis, --simple options)
- **Documentation**
  - Added GPT-5 section to README.md
  - GPT-5 vs Claude 4 comparison table
  - Usage examples and output samples

### Changed
- Version number: 1.1.0 → 1.2.0
- `__init__.py`: Added GPT-5 module and function exports
- Project description: Updated to "Claude 4 + GPT-5 Prompt Optimization Tool"
- Token efficiency: 30-50% → 30-60% (including GPT-5 optimization)

### Technical Details
- **GPT-5 Key Differences**:
  - Highly sensitive to contradictions → Contradiction detection is top priority
  - Agentic workflow-centric → Autonomy and tool usage optimization
  - Parameter control → reasoning_effort, verbosity recommendations
  - XML structure preference → Hierarchical command structure
- **Code Structure**:
  - Claude 4 system fully maintained (backward compatible)
  - GPT-5 modules completely independent (separate files)
  - Both systems available for use

## [1.1.1] - 2025-01-12

### Fixed
- 🔧 **Fixed install.sh GPT-5 Command Installation Issue**
  - Fixed issue where GPT-5 commands were not created during Skills installation
  - Auto-generate GPT-5 commands in `~/.claude/commands/prompt/` directory
  - Added `/analyze-gpt5-prompt` command support
  - Added `/optimize-gpt5-prompt` command support (--include-analysis, --simple flags)

### Changed
- install.sh version: v1.1.0 → v1.1.1
- Added GPT-5 command information to installation completion message

### Technical Details
- GPT-5 commands installed in `~/.claude/commands/prompt/` directory alongside Claude 4 commands
- Backward compatibility maintained: Existing Claude 4 commands remain unchanged

## [1.1.0] - 2025-11-12

### Added
- Global slash commands auto-setup feature
  - Command files automatically created in `~/.claude/commands/prompt` directory during Skills installation
  - Added `/analyze-prompt`: Prompt analysis command
  - Added `/optimize-prompt`: Prompt optimization command
- Added `.gitignore` file to prevent tracking unnecessary files

### Changed
- Improved code formatting (consistent 2-space indentation)
- Enhanced installation script readability and maintainability

### Fixed
- Fixed domain detection and template matching issues
- Improved configuration file update logic

## [1.0.1] - 2025-11-12

### Added
- Added release infrastructure and documentation

### Fixed
- Improved domain detection system
- Fixed template matching logic
- Enhanced settings file update mechanism

## [1.0.0] - 2025-11-12

### Added
- Initial release
- Claude 4 7-principle-based prompt analysis
- Token efficiency optimization (30-50% reduction)
- Domain-specific template system
- Smart improvement recommendations
- Slash command integration (/analyze-prompt, /optimize-prompt)
- Three optimization levels (conservative/balanced/aggressive)
- Domain templates (code/content/analysis/creative)

### Features
- **Analyzer Module**
  - 7-principle score calculation
  - Domain-specific evaluation
  - Context completeness check
  - Clarity and specificity analysis

- **Optimizer Module**
  - Token efficiency optimization
  - Structure improvements
  - Smart recommendations
  - Example-based enhancements

- **Template System**
  - Code review templates
  - Content writing templates
  - Data analysis templates
  - Creative writing templates

### Documentation
- Comprehensive README with usage examples
- Installation guide
- API reference
- Contributing guidelines
