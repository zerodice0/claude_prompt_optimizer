# GPT-5 Prompt Analysis

GPT-5 prompting guide 기반으로 프롬프트를 분석합니다.

## 분석 항목

1. **모순 탐지** - 상충하는 지시사항 식별
2. **Agentic 구조** - 도구 사용, 지속성, escape hatch 평가
3. **파라미터 최적화** - reasoning_effort, verbosity 추천
4. **도구 프리앰블** - 사용자 목표 재구성 포함 여부
5. **명령 명확성** - XML 구조 사용 여부
6. **컨텍스트 효율성** - 과도한 정보 수집 지시 탐지

## Usage

```bash
/analyze-gpt5-prompt "Create a Next.js app with authentication"
```

## Example Output

```
================================================================================
GPT-5 프롬프트 분석 결과
================================================================================

📝 원본 프롬프트:
Create a web application with user authentication

📊 분석 점수:
  • Agentic 구조: 5.0/10
  • 명확성: 5.0/10
  • 컨텍스트 효율성: 7.0/10
  • 도구 프리앰블 품질: 3.0/10
  • 복잡도: 6.5/10

🎯 추천 파라미터:
  • reasoning_effort: medium
  • verbosity: medium
  • XML 구조 사용: 아니오

💡 개선 제안:
  1. 도구 사용 방법을 명시하면 Agentic 구조가 개선됩니다
  2. 작업 지속성 지시를 추가하면 자율성이 향상됩니다
  3. XML 구조를 사용하면 명확성이 크게 향상됩니다
```

## Process

```bash
cd /Users/zerodice0/workspace/zerodice0/development/prompter && python3 -c "
from scripts.gpt5_core import analyze_prompt
import sys

# 명령줄 인수로 프롬프트 받기
prompt = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else input('프롬프트를 입력하세요: ')

# 분석 실행
result = analyze_prompt(prompt)

# 결과 출력
print(result)
" "$@"
```

## Notes

- GPT-5에 특화된 분석 (Claude 4와 다른 접근)
- 모순 탐지가 최우선 (GPT-5는 모순에 매우 민감)
- Agentic workflow 평가
- 파라미터 자동 추천
