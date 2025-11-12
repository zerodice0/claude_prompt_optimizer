# Prompt Optimization

You are a Claude 4 prompt optimization specialist. Optimize the provided prompt to achieve 30-50% token efficiency improvement while maintaining or improving quality.

## 7 Optimization Principles

1. **명확성 (Clarity)**: Make purpose and requirements concrete and specific
2. **컨텍스트 (Context)**: Provide sufficient background information
3. **예시 (Examples)**: Include specific use cases and examples
4. **구조 (Structure)**: Ensure logical order and organization
5. **역할 (Role)**: Clearly define AI persona and expertise
6. **형식 (Format)**: Specify desired output format
7. **제약 (Constraints)**: Explicitly state what to avoid

## Optimization Process

Execute the following Python script to optimize the prompt:

```bash
cd /Users/zerodice0/workspace/zerodice0/development/prompter && python3 -c "
from scripts import optimize_prompt
import sys

# Get prompt from argument or stdin
prompt_text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()

# Optimize the prompt
result = optimize_prompt(prompt_text)

# Display results
if result['success']:
    print('\n✨ 프롬프트 최적화 결과\n')
    print(f'📝 원본: {result[\"original_prompt\"]}\n')
    print(f'✅ 최적화: {result[\"optimized_prompt\"]}\n')

    if result.get('analysis'):
        print(f'📊 원본 총점: {result[\"analysis\"][\"total_score\"]}/35')

    if result.get('optimization'):
        opt = result['optimization']
        print(f'🎯 개선 점수: {opt.get(\"improvement_score\", \"N/A\")}')
        print(f'⚡ 토큰 절감: {opt.get(\"token_reduction\", \"N/A\")}%')

        if opt.get('improvements'):
            print('\n💡 적용된 개선사항:')
            for improvement in opt['improvements']:
                print(f'  • {improvement}')

    if result.get('recommendations'):
        print('\n🔍 추가 권장사항:')
        for rec in result['recommendations']:
            print(f'  • {rec}')

    print(f'\n⏱️  실행 시간: {result[\"execution_time\"]:.2f}초')
    print(f'\n{result[\"message\"]}')
else:
    print(f'❌ 최적화 실패: {result[\"message\"]}')
" "$@"
```

## Output Format

The optimization will provide:

```
✨ 프롬프트 최적화 결과
📝 원본: [원본 프롬프트]
✅ 최적화: [개선된 프롬프트]
📊 원본 총점: [점수]/35
🎯 개선 점수: [개선도]
⚡ 토큰 절감: [절감률]%
💡 적용된 개선사항: [구체적인 개선 내용]
🔍 추가 권장사항: [추가 개선 제안]
```

## Usage Examples

### Basic Optimization
```
/optimize-prompt "코드 리뷰를 부탁드립니다"
```

### With Domain
```
/optimize-prompt "블로그 글을 써줘" --domain=content
```

### With Optimization Level
```
/optimize-prompt "API를 만들어줘" --optimization_level=aggressive
```

## Parameters

- `$1`: The prompt text to optimize
- `--domain`: Target domain (auto, development, marketing, content, business)
- `--optimization_level`: Level of optimization (conservative, balanced, aggressive)

## What This Does

1. Analyzes the original prompt using the 7 principles
2. Identifies weaknesses and improvement opportunities
3. Applies domain-specific optimization strategies
4. Generates an improved prompt with better:
   - Clarity and specificity
   - Context and background
   - Examples and use cases
   - Logical structure
   - Role definition
   - Output format specification
   - Constraint clarification
5. Measures token efficiency improvement
6. Provides actionable recommendations

After running the script, you can directly use the optimized prompt for better results with Claude.
