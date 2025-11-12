# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-12

### Added
- 전역 slash commands 자동 설정 기능
  - Skills 설치 시 `~/.claude/commands/prompt` 디렉토리에 명령어 파일 자동 생성
  - `/analyze-prompt`: 프롬프트 분석 명령어 추가
  - `/optimize-prompt`: 프롬프트 최적화 명령어 추가
- `.gitignore` 파일 추가로 불필요한 파일 추적 방지

### Changed
- 코드 포맷팅 개선 (2-space 들여쓰기로 일관성 향상)
- 설치 스크립트 가독성 및 유지보수성 향상

### Fixed
- 도메인 감지 및 템플릿 매칭 이슈 수정
- 설정 파일 업데이트 로직 개선

## [1.0.1] - 2025-11-12

### Added
- 릴리즈 인프라 및 문서화 추가

### Fixed
- 문서화 개선 및 치명적인 버그 수정

## [1.0.0] - 2025-11-12

### Added
- 초기 릴리즈: Claude Prompt Optimizer v1.0.0
- 7원칙 기반 프롬프트 분석 및 최적화 기능
- Claude Code Skills 통합 지원
- 프로젝트 모드 및 Skills 모드 설치 옵션
- 인터랙티브 설치 스크립트
