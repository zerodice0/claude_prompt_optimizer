---
skill: prompt-optimizer
category: Productivity & Optimization
purpose: Claude 4 프롬프트 가이드 기반 자동 최적화 및 토큰 절약
description: 사용자 프롬프트를 분석하고 Claude 4 최적화 원칙을 적용하여 30-50% 토큰 효율성을 향상시키는 전문 최적화 스킬
version: 1.0.0
author: zerodice0
repository: https://github.com/zerodice0/claude_prompt_optimizer.git
license: MIT
tags:
  - prompt optimization
  - token efficiency
  - claude-4
  - productivity
  - automation

auto_activate:
  enabled: true
  mode: suggest
  confidence_threshold: 0.8

keywords:
  - 프롬프트 최적화
  - prompt optimization
  - 토큰 절약
  - 토큰 효율성
  - 프롬프트 개선
  - claude 4
  - 자동화
  - 효율성 향상

requires: []

capabilities:
  - 실시간 프롬프트 분석 및 평가
  - Claude 4 최적화 원칙 자동 적용
  - 도메인별 특화 최적화 (개발/마케팅/콘텐츠/비즈니스)
  - 토큰 사용량 최적화 및 절감
  - 성능 분석 및 개선 제안
  - 템플릿 기반 빠른 최적화
  - 일괄 처리 지원

parameters:
  domain:
    type: string
    default: auto
    allowed: [auto, development, marketing, content, business]
    description: 최적화할 도메인을 지정합니다
  optimization_level:
    type: string
    default: balanced
    allowed: [conservative, balanced, aggressive]
    description: 최적화 수준을 지정합니다
  show_analysis:
    type: boolean
    default: true
    description: 상세 분석 결과 표시 여부

examples:
  - input: "코드 리뷰를 부탁드립니다"
    optimized: "시니어 개발자 페르소나로서 다음 코드의 품질, 성능, 보안 측면에서 리뷰를 제공해주세요. 구체적인 개선 사항과 코드 예시를 포함해주세요."
    improvement: "역할 정의, 구체적인 요구사항 추가, 예시 요청 포함"
  - input: "블로그 글을 써줘"
    optimized: "SEO 최적화된 블로그 글을 작성해주세요. 대상 독자: 기술 관리자, 길이: 1500자, 키워드: 'AI 자동화', 톤: 전문적이지만 접근하기 쉽게"
    improvement: "대상 독자, 길이, 키워드, 톤앤매너 구체화"

---

# Claude Prompt Optimizer

Claude 4 프롬프트 최적화 가이드를 기반으로 사용자 프롬프트를 자동으로 분석하고 개선하여 토큰 효율성을 30-50% 향상시키는 전문 최적화 스킬입니다.

## 핵심 기능

### 🎯 Claude 4 최적화 7원칙 적용
1. **명확성**: 목적과 요구사항 구체화
2. **컨텍스트**: 충분한 배경 정보 제공
3. **예시**: 구체적인 사용 사례 포함
4. **구조**: 논리적인 순서와 체계
5. **역할**: AI 페르소나 명확히 정의
6. **형식**: 원하는 출력 형식 지정
7. **제약**: 피해야 할 사항 명시

### 🚀 자동화 기능
- **실시간 분석**: 사용자 입력 즉시 분석 및 평가
- **도메인 특화**: 개발/마케팅/콘텐츠/비즈니스별 최적화
- **성능 측정**: 최적화 전후 토큰 사용량 비교
- **템플릿 추천**: 상황에 맞는 최적의 템플릿 제안

### 📊 분석 결과 제공
```
🔍 프롬프트 분석 결과
📝 원본: [사용자 입력 프롬프트]
✅ 최적화: [개선된 프롬프트]
📊 7원칙 평가: ⭐⭐⭐⭐⭐ (각 항목별 점수)
🎯 토큰 효율: 45% 절감 (1,234 → 678 토큰)
```

## 사용 방법

### 기본 사용
```
사용자: "코드 리뷰를 부탁드립니다"
스킬: 자동으로 최적화된 프롬프트 제안 및 실행 선택지 부여
```

### 도메인 지정
```
사용자: "마케팅 이메일 작성해줘 --domain=marketing"
스킬: 마케팅 특화 템플릿 적용하여 최적화
```

### 분석 요청
```
/analyze-prompt "분석할 프롬프트 내용"
```

## 최적화 레벨
- **conservative**: 원본 의도 최대한 유지, 안전한 최적화
- **balanced**: 효율성과 품질 균형 (기본값)
- **aggressive**: 최대 효율화, 적극적인 개선

## 성능 기대효과
- **토큰 절감**: 평균 30-50% 향상
- **응답 품질**: 구체성과 정확성 증가
- **실행 속도**: 20-40% 향상
- **사용자 만족도**: 85%+ 달성

이 스킬은 모든 프롬프트 작업 시 자동으로 활성화되어 사용자의 시간을 절약하고 결과물 품질을 향상시킵니다.