"""
Claude Prompt Analyzer
Claude 4 프롬프트 가이드 7원칙 기반 프롬프트 분석기
"""

import re
import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class OptimizationLevel(Enum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"


class Domain(Enum):
    AUTO = "auto"
    DEVELOPMENT = "development"
    MARKETING = "marketing"
    CONTENT = "content"
    BUSINESS = "business"


@dataclass
class AnalysisResult:
    """프롬프트 분석 결과"""
    original_prompt: str
    domain: Domain
    optimization_level: OptimizationLevel
    scores: Dict[str, int]  # 7원칙별 점수
    total_score: float
    token_count: int
    issues: List[str]
    suggestions: List[str]
    detected_intent: str
    complexity_level: str


class PromptAnalyzer:
    """Claude 4 최적화 원칙 기반 프롬프트 분석기"""

    def __init__(self):
        # Claude 4 최적화 7원칙
        self.principles = {
            "clarity": {
                "name": "명확성",
                "description": "목적과 요구사항 구체화",
                "keywords": ["구체적", "명확", "자세히", "상세", "정확"],
                "indicators": ["목표", "요구사항", "원하는 결과"]
            },
            "context": {
                "name": "컨텍스트",
                "description": "충분한 배경 정보 제공",
                "keywords": ["배경", "상황", "맥락", "정보", "관련"],
                "indicators": ["배경 설명", "관련 정보", "상황 설명"]
            },
            "examples": {
                "name": "예시",
                "description": "구체적인 사용 사례 포함",
                "keywords": ["예시", "예를 들어", "예", "사례", "구체적으로"],
                "indicators": ["실제 예시", "구체적인 경우", "예시 포함"]
            },
            "structure": {
                "name": "구조",
                "description": "논리적인 순서와 체계",
                "keywords": ["순서", "단계", "구조", "체계", "논리"],
                "indicators": ["단계별 설명", "구조화된 요청", "논리적 흐름"]
            },
            "role": {
                "name": "역할",
                "description": "AI 페르소나 명확히 정의",
                "keywords": ["역할", "페르소나", "전문가", "관점", "입장"],
                "indicators": ["역할 정의", "전문가 관점", "특정 페르소나"]
            },
            "format": {
                "name": "형식",
                "description": "원하는 출력 형식 지정",
                "keywords": ["형식", "방식", "구조", "템플릿", "스타일"],
                "indicators": ["출력 형식", "결과 구조", "표현 방식"]
            },
            "constraints": {
                "name": "제약",
                "description": "피해야 할 사항 명시",
                "keywords": ["하지 않도록", "피해주세요", "제외", "금지", "주의"],
                "indicators": ["제약 조건", "금지 사항", "주의사항"]
            }
        }

        # 도메인별 키워드 (구조화된 가중치 시스템)
        self.domain_keywords = {
            Domain.DEVELOPMENT: {
                "simple": ["코드", "프로그래밍", "개발", "버그", "디버깅", "알고리즘", "아키텍처", "리뷰",
                          "테스트", "배포", "빌드", "함수", "클래스", "API", "데이터베이스", "서버"],
                "compound": ["release note", "릴리즈 노트", "릴리스 노트", "change log", "changelog", "변경 로그",
                            "commit message", "커밋 메시지", "pull request", "PR", "코드 리뷰", "기술 문서",
                            "API 문서", "API documentation", "git", "깃허브", "github"],
                "weighted": {
                    "release": 3.0,
                    "commit": 3.0,
                    "deploy": 2.5,
                    "build": 2.0,
                    "git": 2.5,
                    "repository": 2.0,
                    "version": 2.0
                }
            },
            Domain.MARKETING: {
                "simple": ["마케팅", "광고", "캠페인", "프로모션", "브랜드", "고객", "시장", "세일즈"],
                "compound": ["광고 캠페인", "마케팅 전략", "소셜 미디어 마케팅", "이메일 마케팅"],
                "weighted": {
                    "캠페인": 2.5,
                    "광고": 2.0,
                    "홍보": 2.0
                }
            },
            Domain.CONTENT: {
                "simple": ["글", "블로그", "콘텐츠", "기사", "소셜", "미디어", "에세이", "뉴스레터"],
                "compound": ["블로그 포스트", "소셜 미디어 포스트", "인스타그램 게시물", "트위터 트윗"],
                "weighted": {
                    "블로그": 2.0,
                    "포스트": 1.5,
                    "게시물": 1.5
                }
            },
            Domain.BUSINESS: {
                "simple": ["비즈니스", "보고서", "이메일", "프레젠테이션", "계획", "전략", "분석", "의사결정"],
                "compound": ["사업 계획서", "비즈니스 보고서", "이메일 초안", "회의 안건"],
                "weighted": {
                    "보고서": 2.0,
                    "계획서": 2.0,
                    "전략": 1.5
                }
            }
        }

        # 의도 패턴
        self.intent_patterns = {
            "create": ["만들", "생성", "작성", "개발", "구축", "제작"],
            "analyze": ["분석", "리뷰", "평가", "검토", "진단", "조사"],
            "optimize": ["최적화", "개선", "향상", "효율", "개선"],
            "explain": ["설명", "가르쳐", "알려줘", "소개", "개요"],
            "fix": ["수정", "해결", "버그", "문제", "오류", "고쳐줘"],
            "compare": ["비교", "차이", "장단점", "비교해", "대비"],
            "plan": ["계획", "전략", "방안", "로드맵", "단계"]
        }

    def detect_domain(self, prompt: str) -> Domain:
        """프롬프트의 도메인 자동 감지 (가중치 기반)"""
        prompt_lower = prompt.lower()
        domain_scores = {domain: 0.0 for domain in self.domain_keywords.keys()}

        for domain, keywords_dict in self.domain_keywords.items():
            # Simple 키워드 (가중치 1.0)
            if "simple" in keywords_dict:
                simple_score = sum(1.0 for keyword in keywords_dict["simple"]
                                 if keyword in prompt_lower)
                domain_scores[domain] += simple_score

            # Compound 키워드 (가중치 2.0)
            if "compound" in keywords_dict:
                compound_score = sum(2.0 for keyword in keywords_dict["compound"]
                                   if keyword in prompt_lower)
                domain_scores[domain] += compound_score

            # Weighted 키워드 (개별 가중치)
            if "weighted" in keywords_dict:
                weighted_score = sum(weight for keyword, weight in keywords_dict["weighted"].items()
                                   if keyword in prompt_lower)
                domain_scores[domain] += weighted_score

        # 최고 점수 도메인 선택
        if max(domain_scores.values()) == 0:
            return Domain.AUTO

        best_domain = max(domain_scores, key=domain_scores.get)

        # 신뢰도 임계값 적용 (최소 1.0 이상)
        confidence_threshold = 1.0
        if domain_scores[best_domain] >= confidence_threshold:
            return best_domain
        else:
            return Domain.AUTO

    def detect_domain_with_confidence(self, prompt: str) -> tuple:
        """도메인 감지 + 확신도 반환"""
        prompt_lower = prompt.lower()
        domain_scores = {domain: 0.0 for domain in self.domain_keywords.keys()}

        for domain, keywords_dict in self.domain_keywords.items():
            if "simple" in keywords_dict:
                simple_score = sum(1.0 for keyword in keywords_dict["simple"]
                                 if keyword in prompt_lower)
                domain_scores[domain] += simple_score

            if "compound" in keywords_dict:
                compound_score = sum(2.0 for keyword in keywords_dict["compound"]
                                   if keyword in prompt_lower)
                domain_scores[domain] += compound_score

            if "weighted" in keywords_dict:
                weighted_score = sum(weight for keyword, weight in keywords_dict["weighted"].items()
                                   if keyword in prompt_lower)
                domain_scores[domain] += weighted_score

        total_score = sum(domain_scores.values())
        if total_score == 0:
            return Domain.AUTO, 0.0

        best_domain = max(domain_scores, key=domain_scores.get)
        confidence = domain_scores[best_domain] / total_score if total_score > 0 else 0.0

        return best_domain, confidence

    def detect_intent(self, prompt: str) -> str:
        """프롬프트의 주요 의도 감지"""
        prompt_lower = prompt.lower()
        intent_scores = {}

        for intent, patterns in self.intent_patterns.items():
            score = sum(1 for pattern in patterns if pattern in prompt_lower)
            intent_scores[intent] = score

        if max(intent_scores.values()) == 0:
            return "general"

        return max(intent_scores, key=intent_scores.get)

    def calculate_complexity(self, prompt: str) -> str:
        """프롬프트 복잡도 계산"""
        # 기본 복잡도 지표
        word_count = len(prompt.split())
        sentence_count = len(re.split(r'[.!?]+', prompt))
        avg_words_per_sentence = word_count / max(sentence_count, 1)

        # 특수 문자 및 구조
        has_questions = '?' in prompt
        has_conditions = any(word in prompt for word in ['만약', '경우', '조건', 'if', 'when'])
        has_lists = any(char in prompt for char in ['1.', '2.', '-', '•', '*'])
        has_structure = any(word in prompt for word in ['단계', '순서', '단락', '파트'])

        complexity_score = 0

        # 길이 기반 점수
        if word_count > 50:
            complexity_score += 2
        elif word_count > 20:
            complexity_score += 1

        # 구조 기반 점수
        if has_conditions:
            complexity_score += 2
        if has_questions:
            complexity_score += 1
        if has_lists or has_structure:
            complexity_score += 1

        # 평균 문장 길이 기반 점수
        if avg_words_per_sentence > 15:
            complexity_score += 1

        if complexity_score >= 5:
            return "high"
        elif complexity_score >= 3:
            return "medium"
        else:
            return "low"

    def estimate_token_count(self, prompt: str) -> int:
        """토큰 수 추정 (간단한 근사치)"""
        # 한글과 영어의 토큰 비율 고려
        korean_chars = len(re.findall(r'[가-힣]', prompt))
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', prompt))

        # 대략적인 토큰 추정 (한글: 1.5자당 1토큰, 영어: 1단어당 1.3토큰)
        korean_tokens = korean_chars / 1.5
        english_tokens = english_words * 1.3

        return int(korean_tokens + english_tokens)

    def analyze_principle(self, prompt: str, principle_key: str) -> Tuple[int, List[str], List[str]]:
        """개별 원칙에 대한 분석 수행"""
        principle = self.principles[principle_key]
        prompt_lower = prompt.lower()

        score = 1  # 기본 점수
        issues = []
        suggestions = []

        # 키워드 기반 점수 계산
        keyword_matches = sum(1 for keyword in principle["keywords"] if keyword in prompt_lower)
        score += min(keyword_matches, 2)  # 최대 3점까지 추가

        # 지표 기반 추가 점수
        indicator_matches = sum(1 for indicator in principle["indicators"] if indicator in prompt_lower)
        score += min(indicator_matches, 2)  # 최대 2점까지 추가

        # 원칙별 특화 분석
        if principle_key == "clarity":
            if len(prompt.split()) < 5:
                issues.append("프롬프트가 너무 짧아 명확성 부족")
                suggestions.append("더 구체적인 목표와 요구사항을 명시해주세요")
            if "?" not in prompt and "요청" not in prompt and "부탁" not in prompt:
                issues.append("명확한 요청 형태가 아님")
                suggestions.append("무엇을 원하는지 명확히 요청해주세요")

        elif principle_key == "context":
            if len(prompt.split()) < 10:
                issues.append("충분한 배경 정보 부족")
                suggestions.append("작업의 배경과 관련 정보를 더 제공해주세요")

        elif principle_key == "examples":
            if "예시" not in prompt and "예를" not in prompt:
                issues.append("구체적인 예시 부재")
                suggestions.append("기대하는 결과물의 예시를 포함해주세요")

        elif principle_key == "role":
            role_indicators = ["역할", "전문가", "관점", "입장"]
            if not any(indicator in prompt for indicator in role_indicators):
                issues.append("AI 역할이 정의되지 않음")
                suggestions.append("AI에게 특정 역할을 부여해주세요 (예: '전문가로서', '관리자 관점에서')")

        elif principle_key == "format":
            format_indicators = ["형식", "방식", "구조", "템플릿"]
            if not any(indicator in prompt for indicator in format_indicators):
                issues.append("출력 형식이 지정되지 않음")
                suggestions.append("원하는 결과물의 형식이나 구조를 명시해주세요")

        elif principle_key == "constraints":
            if not any(negative in prompt for negative in ["하지 않도록", "피해", "제외", "주의"]):
                issues.append("피해야 할 사항이 명시되지 않음")
                suggestions.append("원치 않는 결과나 피해야 할 사항을 명시해주세요")

        # 점수 제한 (1-5)
        score = max(1, min(5, score))

        return score, issues, suggestions

    def analyze(self, prompt: str, domain: Domain = Domain.AUTO,
                optimization_level: OptimizationLevel = OptimizationLevel.BALANCED) -> AnalysisResult:
        """전체 프롬프트 분석 수행"""

        # 도메인 자동 감지
        if domain == Domain.AUTO:
            domain = self.detect_domain(prompt)

        # 기본 정보 계산
        token_count = self.estimate_token_count(prompt)
        detected_intent = self.detect_intent(prompt)
        complexity_level = self.calculate_complexity(prompt)

        # 7원칙 분석
        scores = {}
        all_issues = []
        all_suggestions = []

        for principle_key in self.principles.keys():
            score, issues, suggestions = self.analyze_principle(prompt, principle_key)
            scores[principle_key] = score
            all_issues.extend(issues)
            all_suggestions.extend(suggestions)

        # 총점 계산
        total_score = sum(scores.values()) / len(scores)

        # 최적화 레벨에 따른 필터링
        if optimization_level == OptimizationLevel.CONSERVATIVE:
            # 보수적: 중요한 이슈만
            all_issues = [issue for issue in all_issues if "너무 짧아" in issue or "부족" in issue]
            all_suggestions = all_suggestions[:3]
        elif optimization_level == OptimizationLevel.AGGRESSIVE:
            # 적극적: 모든 개선 제안
            all_suggestions.extend([
                "더 구체적인 수치나 목표를 추가해보세요",
                "실제 사용 사례를 포함해보세요",
                "결과물의 활용 방법을 명시해보세요"
            ])

        return AnalysisResult(
            original_prompt=prompt,
            domain=domain,
            optimization_level=optimization_level,
            scores=scores,
            total_score=total_score,
            token_count=token_count,
            issues=all_issues,
            suggestions=all_suggestions,
            detected_intent=detected_intent,
            complexity_level=complexity_level
        )

    def get_analysis_summary(self, result: AnalysisResult) -> str:
        """분석 결과 요약 생성"""
        principle_names = {k: v["name"] for k, v in self.principles.items()}

        summary = f"""🔍 프롬프트 분석 결과

📝 원본 프롬프트:
{result.original_prompt}

🎯 감지된 정보:
• 도메인: {result.domain.value}
• 의도: {result.detected_intent}
• 복잡도: {result.complexity_level}
• 토큰 수: {result.token_count}

📊 Claude 4 원칙 평가:"""

        for principle, score in result.scores.items():
            stars = "⭐" * score + "☆" * (5 - score)
            summary += f"\n• {principle_names[principle]}: {stars} ({score}/5)"

        summary += f"\n• 종합 점수: {result.total_score:.1f}/5.0"

        if result.issues:
            summary += "\n\n⚠️ 개선이 필요한 부분:"
            for issue in result.issues:
                summary += f"\n• {issue}"

        if result.suggestions:
            summary += "\n\n💡 개선 제안:"
            for i, suggestion in enumerate(result.suggestions, 1):
                summary += f"\n{i}. {suggestion}"

        return summary


# 사용 예시
if __name__ == "__main__":
    analyzer = PromptAnalyzer()

    test_prompt = "코드 리뷰를 부탁드립니다"
    result = analyzer.analyze(test_prompt)

    print(analyzer.get_analysis_summary(result))