# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-01-12

### Added
- 🆕 **GPT-5 프롬프트 최적화 지원**
  - GPT-5 prompting guide 기반 전문 최적화 엔진
  - `gpt5_analyzer.py`: GPT-5 특화 분석기
    - 모순 탐지 (GPT-5는 모순에 매우 민감)
    - Agentic 구조 평가 (도구 사용, 지속성, escape hatch)
    - 파라미터 자동 추천 (reasoning_effort, verbosity)
    - 도구 프리앰블 품질 평가
    - 컨텍스트 효율성 분석
  - `gpt5_optimizer.py`: GPT-5 최적화기
    - 모순 자동 제거 및 통합
    - XML 구조화 (계층적 프롬프트)
    - 도구 프리앰블 자동 추가
    - Agentic 패턴 적용 (eagerness 제어)
    - Anti-pattern 자동 수정
  - `gpt5_core.py`: 통합 엔진
    - 분석 + 최적화 파이프라인
    - 간편 API 함수
  - `gpt5_patterns.json`: GPT-5 패턴 라이브러리
    - Agentic 패턴 (low/medium/high eagerness)
    - XML 템플릿 (basic, agentic, code_editing)
    - 모순 패턴 사전
    - Anti-pattern 정의 및 수정 전략
- **새로운 Slash Commands**
  - `/analyze-gpt5-prompt`: GPT-5 특화 분석
  - `/optimize-gpt5-prompt`: GPT-5 최적화 (--include-analysis, --simple 옵션 지원)
- **문서화**
  - README.md에 GPT-5 섹션 추가
  - GPT-5 vs Claude 4 비교표
  - 사용 예시 및 출력 샘플

### Changed
- 버전 번호: 1.1.0 → 1.2.0
- `__init__.py`: GPT-5 모듈 및 함수 export 추가
- 프로젝트 설명: "Claude 4 + GPT-5 프롬프트 최적화 도구"로 업데이트
- 토큰 효율성: 30-50% → 30-60% (GPT-5 최적화 포함)

### Technical Details
- **GPT-5 핵심 차이점**:
  - 모순에 매우 민감 → 모순 탐지가 최우선
  - Agentic workflow 중심 → 자율성, 도구 사용 최적화
  - 파라미터 제어 → reasoning_effort, verbosity 추천
  - XML 구조 선호 → 계층적 명령 구조
- **코드 구조**:
  - Claude 4 시스템 완전히 유지 (backward compatible)
  - GPT-5 모듈 완전 독립 (별도 파일)
  - 두 시스템 모두 사용 가능

## [1.1.1] - 2025-01-12

### Fixed
- 🔧 **install.sh GPT-5 커맨드 설치 누락 문제 해결**
  - Skills 설치 시 GPT-5 커맨드가 생성되지 않던 문제 수정
  - `~/.claude/commands/prompt/` 디렉토리에 GPT-5 커맨드 자동 생성
  - `/analyze-gpt5-prompt` 커맨드 설치 지원
  - `/optimize-gpt5-prompt` 커맨드 설치 지원 (--include-analysis, --simple 플래그 포함)

### Changed
- install.sh 버전: v1.1.0 → v1.1.1
- 설치 완료 메시지에 GPT-5 커맨드 정보 추가

### Technical Details
- GPT-5 커맨드는 `~/.claude/commands/prompt/` 디렉토리에 설치되어 Claude 4 커맨드와 함께 동작
- 하위 호환성 유지: 기존 Claude 4 커맨드는 그대로 유지

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
