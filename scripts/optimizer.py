"""
Claude Prompt Optimizer
Claude 4 가이드 기반 프롬프트 최적화 엔진
"""

import re
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from .analyzer import AnalysisResult, Domain, OptimizationLevel


@dataclass
class OptimizationResult:
    """최적화 결과"""
    original_prompt: str
    optimized_prompt: str
    improvement_areas: List[str]
    token_reduction: int
    token_reduction_percent: float
    optimization_score: float
    applied_techniques: List[str]


class PromptOptimizer:
    """Claude 4 프롬프트 최적화 엔진"""

    def __init__(self):
        # 역할 템플릿
        self.role_templates = {
            "development": {
                "expert": "시니어 개발자로서",
                "reviewer": "코드 리뷰 전문가로서",
                "architect": "소프트웨어 아키텍트로서",
                "debugger": "디버깅 전문가로서"
            },
            "marketing": {
                "expert": "마케팅 전문가로서",
                "strategist": "마케팅 전략가로서",
                "copywriter": "카피라이터로서",
                "analyst": "마켓 분석가로서"
            },
            "content": {
                "expert": "콘텐츠 전문가로서",
                "writer": "전문 작가로서",
                "editor": "에디터로서",
                "creator": "콘텐츠 크리에이터로서"
            },
            "business": {
                "expert": "비즈니스 전문가로서",
                "analyst": "비즈니스 분석가로서",
                "strategist": "전략 컨설턴트로서",
                "consultant": "경영 컨설턴트로서"
            }
        }

        # 형식 템플릿
        self.format_templates = {
            "structured": "구조화된 형식으로",
            "step_by_step": "단계별로 설명해서",
            "bullet_points": "핵심 포인트별로 정리해서",
            "table_format": "표 형식으로",
            "code_blocks": "코드 블록을 포함해서",
            "examples": "구체적인 예시와 함께"
        }

        # 개선 템플릿
        self.improvement_patterns = {
            "specificity": [
                "구체적인 {metric}을 포함해서",
                "{number}가지 핵심 요소를 중심으로",
                "실제 사례를 바탕으로"
            ],
            "context": [
                "{context} 관점에서",
                "{background} 배경을 고려해서",
                "실무적인 관점에서"
            ],
            "actionability": [
                "즉시 적용 가능한",
                "실용적인",
                "실행 가능한"
            ]
        }

        # 토큰 최적화 패턴
        self.token_optimization_patterns = [
            (r'자세히\s*설명해주세요', '설명해주세요'),
            (r'상세히\s*알려주세요', '알려주세요'),
            (r'가능한\s*자세히', '자세히'),
            (r'차근차근\s*설명해서', '설명해서'),
            (r'친절하게\s*설명해줘', '설명해줘'),
            (r'자세히\s*설명해주시면\s*감사하겠습니다', '설명해주세요'),
            (r'궁금하니까\s*알려줘', '알려줘'),
            (r'제가\s*이해할\s*수\s*있도록', ''),
            (r'초보자도\s*이해할\s*수 있도록', '쉽게'),
            (r'전문적인\s*관점에서', '전문가로서'),
            (r'체계적으로\s*정리해서', '정리해서'),
            (r'논리적으로\s*설명해서', '설명해서'),
            (r'단계별로\s*나누어서', '단계별로'),
            (r'실제\s*사례를\s*통해', '예시와 함께'),
        ]

    def optimize_clarity(self, prompt: str, analysis: AnalysisResult) -> Tuple[str, List[str]]:
        """명확성 최적화"""
        optimized = prompt
        improvements = []

        # 구체성 부족 시 개선
        if analysis.scores.get("clarity", 0) < 4:
            if len(prompt.split()) < 5:
                optimized = f"구체적인 목표를 가지고 {optimized}"
                improvements.append("구체적인 목표 추가")

            # 애매한 표현 제거
            vague_expressions = ["좀", "좀 더", "조금", "약간", "대충", "大概り"]
            for expr in vague_expressions:
                if expr in optimized:
                    optimized = optimized.replace(expr, "")
                    improvements.append(f"애매한 표현 '{expr}' 제거")

        # 명확한 요청 형태로 변환
        if not any(ending in optimized for ending in ["주세요", "해주세요", "해줘", "부탁드립니다"]):
            if "?" not in optimized:
                optimized += "를 제공해주세요"
                improvements.append("명확한 요청 형식 추가")

        return optimized, improvements

    def optimize_role(self, prompt: str, domain: Domain, analysis: AnalysisResult) -> Tuple[str, List[str]]:
        """역할 정의 최적화"""
        optimized = prompt
        improvements = []

        # 역할 점수가 낮을 경우 역할 추가
        if analysis.scores.get("role", 0) < 4:
            domain_roles = self.role_templates.get(domain.value, self.role_templates["development"])

            # 의도에 따른 역할 선택
            intent = analysis.detected_intent
            if intent == "create":
                role = domain_roles.get("expert", "전문가로서")
            elif intent == "analyze" or intent == "review":
                role = domain_roles.get("analyst", "분석가로서")
            elif intent == "fix":
                role = domain_roles.get("debugger", "전문가로서")
            else:
                role = domain_roles.get("expert", "전문가로서")

            optimized = f"{role} {optimized}"
            improvements.append(f"역할 정의: {role}")

        return optimized, improvements

    def optimize_context(self, prompt: str, domain: Domain, analysis: AnalysisResult) -> Tuple[str, List[str]]:
        """컨텍스트 최적화"""
        optimized = prompt
        improvements = []

        # 컨텍스트 점수가 낮을 경우 배경 정보 추가
        if analysis.scores.get("context", 0) < 4:
            context_templates = {
                Domain.DEVELOPMENT: "실제 개발 환경에서 사용되는 코드를 고려하여",
                Domain.MARKETING: "실제 비즈니스 상황과 타겟 고객을 고려하여",
                Domain.CONTENT: "실제 독자의 관심사와 검색 의도를 고려하여",
                Domain.BUSINESS: "실제 비즈니스 의사결정 과정을 고려하여"
            }

            context = context_templates.get(domain, "")
            if context and context not in optimized:
                optimized = f"{context} {optimized}"
                improvements.append("실용적인 컨텍스트 추가")

        return optimized, improvements

    def optimize_examples(self, prompt: str, analysis: AnalysisResult) -> Tuple[str, List[str]]:
        """예시 최적화"""
        optimized = prompt
        improvements = []

        # 예시 점수가 낮을 경우 예시 요청 추가
        if analysis.scores.get("examples", 0) < 4:
            if "예시" not in optimized and "예" not in optimized:
                optimized += " 구체적인 예시를 포함해주세요"
                improvements.append("구체적인 예시 요청 추가")

        return optimized, improvements

    def optimize_format(self, prompt: str, analysis: AnalysisResult) -> Tuple[str, List[str]]:
        """형식 최적화"""
        optimized = prompt
        improvements = []

        # 형식 점수가 낮을 경우 형식 지정
        if analysis.scores.get("format", 0) < 4:
            # 복잡도에 따른 형식 추천
            if analysis.complexity_level == "high":
                format_guide = "구조화된 형식으로 각 항목을 명확히 구분해서"
                improvements.append("구조화된 형식 지정")
            elif analysis.complexity_level == "medium":
                format_guide = "핵심 포인트별로 정리해서"
                improvements.append "핵심 포인트별 정리"
            else:
                format_guide = "명확하고 간결하게"
                improvements.append("간결한 형식 지정")

            if "형식" not in optimized and "구조" not in optimized:
                optimized += f" {format_guide}"
                improvements.append("출력 형식 지정")

        return optimized, improvements

    def optimize_constraints(self, prompt: str, analysis: AnalysisResult) -> Tuple[str, List[str]]:
        """제약 조건 최적화"""
        optimized = prompt
        improvements = []

        # 제약 조건 점수가 낮을 경우 피해야 할 사항 추가
        if analysis.scores.get("constraints", 0) < 4 and analysis.optimization_level != OptimizationLevel.CONSERVATIVE:
            constraint_templates = [
                "불필요한 기술 용어는 피해주세요",
                "실용적이지 않은 내용은 제외해주세요",
                "지나치게 이론적인 설명은 자제해주세요"
            ]

            # 도메인별 특화 제약 조건
            domain_constraints = {
                Domain.DEVELOPMENT: "실제 사용되지 않는 코드 예시는 포함하지 말아주세요",
                Domain.MARKETING: "과장된 표현은 피해주세요",
                Domain.CONTENT: "선정적인 표현은 자제해주세요",
                Domain.BUSINESS: "실현 불가능한 제안은 제외해주세요"
            }

            if analysis.optimization_level == OptimizationLevel.AGGRESSIVE:
                # 적극적 최적화 시 모든 제약 조건 추가
                constraints = constraint_templates + [domain_constraints.get(analysis.domain, "")]
            else:
                # 균형 잡힌 최적화 시 핵심 제약 조건만
                constraints = [constraint_templates[0]]

            for constraint in constraints:
                if constraint and constraint not in optimized:
                    optimized += f", {constraint}"
                    improvements.append("제약 조건 추가")

        return optimized, improvements

    def optimize_tokens(self, prompt: str) -> Tuple[str, int]:
        """토큰 효율성 최적화"""
        optimized = prompt
        original_tokens = self.estimate_tokens(prompt)
        total_reduction = 0

        # 토큰 최적화 패턴 적용
        for pattern, replacement in self.token_optimization_patterns:
            if re.search(pattern, optimized):
                before_tokens = self.estimate_tokens(optimized)
                optimized = re.sub(pattern, replacement, optimized)
                after_tokens = self.estimate_tokens(optimized)
                reduction = before_tokens - after_tokens
                total_reduction += reduction

        # 중복 표현 제거
        duplicated_patterns = [
            (r'자세히\s*설명해줘서\s*감사합니다', '설명해주세요'),
            (r'알려주셔서\s*감사합니다', '알려주세요'),
            (r'부탁드립니다\.?\s*감사합니다', '부탁드립니다'),
            (r'친절한\s*설명에\s*감사드립니다', '설명해주세요'),
        ]

        for pattern, replacement in duplicated_patterns:
            if re.search(pattern, optimized):
                before_tokens = self.estimate_tokens(optimized)
                optimized = re.sub(pattern, replacement, optimized)
                after_tokens = self.estimate_tokens(optimized)
                total_reduction += (before_tokens - after_tokens)

        return optimized, total_reduction

    def estimate_tokens(self, text: str) -> int:
        """간단한 토큰 수 추정"""
        korean_chars = len(re.findall(r'[가-힣]', text))
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        korean_tokens = korean_chars / 1.5
        english_tokens = english_words * 1.3
        return int(korean_tokens + english_tokens)

    def optimize(self, analysis: AnalysisResult) -> OptimizationResult:
        """전체 최적화 수행"""
        optimized_prompt = analysis.original_prompt
        all_improvements = []
        applied_techniques = []

        # 단계별 최적화 수행
        # 1. 명확성 최적화
        optimized_prompt, improvements = self.optimize_clarity(optimized_prompt, analysis)
        all_improvements.extend(improvements)
        if improvements:
            applied_techniques.append("명확성 향상")

        # 2. 역할 정의 최적화
        optimized_prompt, improvements = self.optimize_role(optimized_prompt, analysis.domain, analysis)
        all_improvements.extend(improvements)
        if improvements:
            applied_techniques.append("역할 정의")

        # 3. 컨텍스트 최적화
        optimized_prompt, improvements = self.optimize_context(optimized_prompt, analysis.domain, analysis)
        all_improvements.extend(improvements)
        if improvements:
            applied_techniques.append("컨텍스트 강화")

        # 4. 예시 최적화
        optimized_prompt, improvements = self.optimize_examples(optimized_prompt, analysis)
        all_improvements.extend(improvements)
        if improvements:
            applied_techniques.append("예시 요청")

        # 5. 형식 최적화
        optimized_prompt, improvements = self.optimize_format(optimized_prompt, analysis)
        all_improvements.extend(improvements)
        if improvements:
            applied_techniques.append("형식 지정")

        # 6. 제약 조건 최적화
        optimized_prompt, improvements = self.optimize_constraints(optimized_prompt, analysis)
        all_improvements.extend(improvements)
        if improvements:
            applied_techniques.append("제약 조건")

        # 7. 토큰 최적화
        token_optimized, token_reduction = self.optimize_tokens(optimized_prompt)
        optimized_prompt = token_optimized

        if token_reduction > 0:
            applied_techniques.append("토큰 효율화")

        # 최종 정리
        optimized_prompt = re.sub(r'\s+', ' ', optimized_prompt).strip()
        optimized_prompt = optimized_prompt.replace(",,", ",").replace(",,", ",")

        # 최적화 점수 계산
        original_tokens = analysis.token_count
        final_tokens = self.estimate_tokens(optimized_prompt)
        actual_reduction = original_tokens - final_tokens
        reduction_percent = (actual_reduction / original_tokens * 100) if original_tokens > 0 else 0

        # 품질 향상 점수 (분석 개선 + 토큰 절감)
        analysis_improvement = len([imp for imp in all_improvements if "추가" in imp or "향상" in imp])
        token_efficiency = min(5, max(1, int(reduction_percent / 10)))
        optimization_score = min(5, (analysis_improvement + token_efficiency) / 2)

        return OptimizationResult(
            original_prompt=analysis.original_prompt,
            optimized_prompt=optimized_prompt,
            improvement_areas=all_improvements,
            token_reduction=actual_reduction,
            token_reduction_percent=reduction_percent,
            optimization_score=optimization_score,
            applied_techniques=applied_techniques
        )

    def get_optimization_summary(self, result: OptimizationResult) -> str:
        """최적화 결과 요약"""
        summary = f"""✅ 최적화된 프롬프트:
{result.optimized_prompt}

🎯 최적화 결과:
• 토큰 절감: {result.token_reduction_percent:.1f}% ({result.token_reduction} 토큰)
• 적용 기법: {', '.join(result.applied_techniques)}
• 최적화 점수: {result.optimization_score:.1f}/5.0"""

        if result.improvement_areas:
            summary += "\n\n🔧 개선 사항:"
            for improvement in result.improvement_areas:
                summary += f"\n• {improvement}"

        return summary


# 사용 예시
if __name__ == "__main__":
    from .analyzer import PromptAnalyzer, Domain, OptimizationLevel

    analyzer = PromptAnalyzer()
    optimizer = PromptOptimizer()

    test_prompt = "코드 리뷰를 부탁드립니다"
    analysis = analyzer.analyze(test_prompt, Domain.AUTO, OptimizationLevel.BALANCED)
    optimization = optimizer.optimize(analysis)

    print(optimizer.get_optimization_summary(optimization))