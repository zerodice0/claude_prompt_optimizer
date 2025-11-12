# GPT-5 Prompt Optimization

GPT-5 prompting guide 기반으로 프롬프트를 최적화합니다.

## 최적화 기법

1. **모순 제거** - 상충하는 지시사항 통합 및 우선순위 명확화
2. **XML 구조화** - 계층적 프롬프트 구조 적용
3. **파라미터 추천** - reasoning_effort, verbosity 자동 설정
4. **Agentic 패턴 적용** - eagerness 조정, escape hatch 추가
5. **도구 프리앰블 삽입** - 목표 재구성, 진행 상황 업데이트
6. **Anti-pattern 수정** - GPT-5 안티패턴 제거

## Usage

```bash
# 기본 최적화
/optimize-gpt5-prompt "Create authentication system"

# 분석 결과 포함
/optimize-gpt5-prompt "Implement user dashboard" --include-analysis

# 간단한 출력 (최적화된 프롬프트만)
/optimize-gpt5-prompt "Build REST API" --simple
```

## Example Output

```
================================================================================
GPT-5 프롬프트 최적화 결과
================================================================================

📝 원본 프롬프트:
Never proceed without confirmation but also auto-schedule immediately

🔧 적용된 개선사항:
  1. 모순 제거: 권한 관련 모순 → 우선순위 명시
  2. Anti-pattern 수정: 과도한 철저함 강조
  3. 도구 프리앰블 추가
  4. Agentic 패턴 적용: medium_eagerness
  5. Verbosity 최적화: 균형잡힌 응답
  6. XML 구조 생성

✅ 최적화된 프롬프트:
Only schedule after obtaining confirmation, except in emergency situations.
Gather sufficient and relevant context.

## Tool Usage Guidelines
- Rephrase the user's goal in a friendly, clear manner
- Outline a structured plan
- Provide progress updates

## Agentic Behavior (균형잡힌 탐색)
- Balance thoroughness with efficiency
- Confirm critical decisions with user
- Document key assumptions clearly

🎯 권장 파라미터:
  reasoning_effort: medium
  verbosity: medium
  model: gpt-4
```

## Process

```bash
cd /Users/zerodice0/workspace/zerodice0/development/prompter && python3 -c "
from scripts.gpt5_core import analyze_and_optimize_prompt
import sys

# 명령줄 인수 파싱
args = sys.argv[1:]
include_analysis = '--include-analysis' in args
simple_mode = '--simple' in args

# 플래그 제거
args = [arg for arg in args if not arg.startswith('--')]

# 프롬프트 받기
prompt = ' '.join(args) if args else input('프롬프트를 입력하세요: ')

# 최적화 실행
if simple_mode:
    from scripts.gpt5_core import GPT5Engine
    engine = GPT5Engine()
    result = engine.optimize(prompt)
    print('✅ 최적화된 프롬프트:')
    print('=' * 80)
    print(result.optimized_prompt)
    print()
    print('🎯 권장 파라미터:')
    for key, value in result.parameter_config.items():
        print(f'  {key}: {value}')
else:
    result = analyze_and_optimize_prompt(prompt, include_analysis=include_analysis)
    print(result)
" "$@"
```

## Options

- `--include-analysis`: 분석 결과도 함께 출력
- `--simple`: 최적화된 프롬프트와 파라미터만 출력

## Notes

- GPT-5에 특화된 최적화 (Claude 4와 다른 접근)
- 모순 자동 제거
- XML 구조 자동 생성
- Agentic 패턴 자동 적용
- Anti-pattern 자동 수정
