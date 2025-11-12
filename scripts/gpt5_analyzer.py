"""
GPT-5 Prompt Analyzer
GPT-5 특화 프롬프트 분석기

GPT-5 prompting guide 기반으로 프롬프트를 분석합니다:
- 모순 탐지
- Agentic 구조 평가
- 파라미터 추천 (reasoning_effort, verbosity)
- 도구 프리앰블 품질
- XML 구조 검사
"""

import re
import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class ReasoningEffort(Enum):
    """Reasoning effort 레벨"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Verbosity(Enum):
    """Verbosity 레벨"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Severity(Enum):
    """이슈 심각도"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Contradiction:
    """모순 정보"""
    pattern: str
    description: str
    example: str
    severity: str
    location: str
    fix_strategy: str


@dataclass
class GPT5AnalysisResult:
    """GPT-5 분석 결과"""
    original_prompt: str
    contradictions: List[Contradiction]
    agentic_score: float  # 0-10
    clarity_score: float  # 0-10
    context_efficiency_score: float  # 0-10
    tool_preamble_quality: float  # 0-10
    reasoning_effort_recommendation: str
    verbosity_recommendation: str
    xml_structured: bool
    issues: List[Dict[str, str]]
    suggestions: List[str]
    complexity_score: float  # 0-10

    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        result = asdict(self)
        # Contradiction 객체들을 딕셔너리로 변환
        result['contradictions'] = [asdict(c) for c in self.contradictions]
        return result


class GPT5PromptAnalyzer:
    """GPT-5 전용 프롬프트 분석기"""

    def __init__(self, patterns_file: Optional[str] = None):
        """
        초기화

        Args:
            patterns_file: GPT-5 패턴 파일 경로 (None이면 기본 경로 사용)
        """
        if patterns_file is None:
            # 기본 패턴 파일 경로
            current_dir = Path(__file__).parent
            patterns_file = current_dir.parent / "references" / "patterns" / "gpt5_patterns.json"

        with open(patterns_file, 'r', encoding='utf-8') as f:
            self.patterns = json.load(f)

    def detect_contradictions(self, prompt: str) -> List[Contradiction]:
        """
        모순되는 지시사항 탐지

        Args:
            prompt: 분석할 프롬프트

        Returns:
            감지된 모순 리스트
        """
        contradictions = []
        prompt_lower = prompt.lower()

        for pattern_info in self.patterns['contradiction_patterns']['common_contradictions']:
            patterns = pattern_info['pattern']

            # 두 패턴이 모두 존재하는지 확인
            matches = []
            for p in patterns:
                match = re.search(p, prompt_lower, re.IGNORECASE)
                if match:
                    matches.append((match.group(), match.start()))

            # 두 패턴이 모두 발견되면 모순
            if len(matches) >= 2:
                location = f"위치: {matches[0][1]}, {matches[1][1]}"
                contradictions.append(Contradiction(
                    pattern=" vs ".join(patterns),
                    description=pattern_info['description'],
                    example=pattern_info['example'],
                    severity=pattern_info['severity'],
                    location=location,
                    fix_strategy=pattern_info['fix_strategy']
                ))

        # 절대 금지 + 절대 필수 키워드 조합 검사
        prohibitions = self.patterns['contradiction_patterns']['detection_keywords']['absolute_prohibitions']
        requirements = self.patterns['contradiction_patterns']['detection_keywords']['absolute_requirements']

        for prohibition in prohibitions:
            for requirement in requirements:
                if prohibition in prompt_lower and requirement in prompt_lower:
                    # 같은 문맥에서 나타나는지 확인 (50자 이내)
                    prohibition_pos = prompt_lower.find(prohibition)
                    requirement_pos = prompt_lower.find(requirement)

                    if abs(prohibition_pos - requirement_pos) < 100:
                        contradictions.append(Contradiction(
                            pattern=f"{prohibition} vs {requirement}",
                            description="절대 금지와 절대 필수의 모순",
                            example=f"문맥에 '{prohibition}'와 '{requirement}'가 함께 나타남",
                            severity="high",
                            location=f"위치: {min(prohibition_pos, requirement_pos)}",
                            fix_strategy="명확한 우선순위 설정 또는 조건부 로직 추가"
                        ))

        return contradictions

    def analyze_agentic_structure(self, prompt: str) -> Tuple[float, List[str]]:
        """
        Agentic 구조 평가

        Args:
            prompt: 분석할 프롬프트

        Returns:
            (agentic_score, suggestions): 점수(0-10)와 개선 제안
        """
        score = 5.0  # 기본 점수
        suggestions = []

        # 1. 도구 사용 명시 여부 (+2점)
        tool_keywords = ['tool', 'function', 'api', 'call', '도구', '함수']
        if any(keyword in prompt.lower() for keyword in tool_keywords):
            score += 2
        else:
            suggestions.append("도구 사용 방법을 명시하면 Agentic 구조가 개선됩니다")

        # 2. 지속성 지시 여부 (+2점)
        persistence_keywords = ['continue', 'keep going', 'until', 'completely', '계속', '끝까지']
        if any(keyword in prompt.lower() for keyword in persistence_keywords):
            score += 2
        else:
            suggestions.append("작업 지속성 지시를 추가하면 자율성이 향상됩니다")

        # 3. Escape hatch 존재 여부 (+1점)
        escape_keywords = ['if uncertain', 'if unsure', 'best judgment', '불확실하면', '판단']
        if any(keyword in prompt.lower() for keyword in escape_keywords):
            score += 1
        else:
            suggestions.append("불확실성 처리 방법(escape hatch)을 추가하세요")

        # 4. 과도한 철저함 강조 (-2점)
        over_thorough = ['maximize', 'all possible', 'every single', '모든', '완벽하게']
        if sum(1 for keyword in over_thorough if keyword in prompt.lower()) >= 3:
            score -= 2
            suggestions.append("과도한 철저함 강조는 불필요한 도구 과다 사용을 유발합니다")

        return max(0, min(10, score)), suggestions

    def analyze_clarity(self, prompt: str) -> Tuple[float, List[str]]:
        """
        명령 명확성 평가

        Args:
            prompt: 분석할 프롬프트

        Returns:
            (clarity_score, suggestions): 점수(0-10)와 개선 제안
        """
        score = 5.0
        suggestions = []

        # 1. XML 구조 사용 (+3점)
        if '<' in prompt and '>' in prompt:
            xml_tags = re.findall(r'<(\w+)>', prompt)
            if len(xml_tags) >= 2:
                score += 3
            else:
                score += 1.5
                suggestions.append("더 체계적인 XML 구조를 사용하세요")
        else:
            suggestions.append("XML 구조를 사용하면 명확성이 크게 향상됩니다")

        # 2. 구조화된 섹션 (+2점)
        section_indicators = ['##', '1.', '2.', 'Step', '단계']
        if sum(1 for ind in section_indicators if ind in prompt) >= 2:
            score += 2
        else:
            suggestions.append("번호나 제목으로 섹션을 구분하세요")

        # 3. 애매한 표현 (-1점)
        ambiguous = ['as needed', 'when appropriate', 'if necessary', '필요하면', '적절히']
        ambiguous_count = sum(1 for word in ambiguous if word in prompt.lower())
        if ambiguous_count > 2:
            score -= ambiguous_count * 0.5
            suggestions.append(f"애매한 표현({ambiguous_count}개)을 구체적으로 바꾸세요")

        return max(0, min(10, score)), suggestions

    def analyze_context_efficiency(self, prompt: str) -> Tuple[float, List[str]]:
        """
        컨텍스트 효율성 평가

        Args:
            prompt: 분석할 프롬프트

        Returns:
            (efficiency_score, suggestions): 점수(0-10)와 개선 제안
        """
        score = 7.0  # 기본 점수
        suggestions = []

        # 과도한 정보 수집 지시 (-3점)
        excessive = ['maximize context', 'all possible information', 'gather everything',
                     'read all files', '모든 정보', '모든 파일']
        excessive_count = sum(1 for phrase in excessive if phrase in prompt.lower())
        if excessive_count > 0:
            score -= excessive_count * 1.5
            suggestions.append("과도한 컨텍스트 수집 지시는 토큰을 낭비합니다")

        # 균형잡힌 접근 (+2점)
        balanced = ['sufficient', 'relevant', 'necessary', '필요한', '관련된']
        if any(word in prompt.lower() for word in balanced):
            score += 2
        else:
            suggestions.append("'sufficient' 또는 'relevant' 같은 균형잡힌 표현을 사용하세요")

        return max(0, min(10, score)), suggestions

    def analyze_tool_preamble(self, prompt: str) -> Tuple[float, List[str]]:
        """
        도구 프리앰블 품질 평가

        Args:
            prompt: 분석할 프롬프트

        Returns:
            (quality_score, suggestions): 점수(0-10)와 개선 제안
        """
        score = 3.0  # 기본 점수 (프리앰블 없으면 낮음)
        suggestions = []

        # 목표 재구성 요청 (+2점)
        restate_keywords = ['rephrase', 'restate', 'clarify goal', '재구성', '명확히']
        if any(keyword in prompt.lower() for keyword in restate_keywords):
            score += 2
        else:
            suggestions.append("사용자 목표를 재구성하도록 요청하세요")

        # 계획 작성 요청 (+2점)
        plan_keywords = ['plan', 'outline', 'steps', '계획', '단계']
        if any(keyword in prompt.lower() for keyword in plan_keywords):
            score += 2
        else:
            suggestions.append("구조화된 계획을 작성하도록 요청하세요")

        # 진행 상황 업데이트 요청 (+3점)
        progress_keywords = ['progress', 'update', 'status', '진행', '상황']
        if any(keyword in prompt.lower() for keyword in progress_keywords):
            score += 3
        else:
            suggestions.append("진행 상황 업데이트를 요청하세요")

        return max(0, min(10, score)), suggestions

    def calculate_complexity(self, prompt: str) -> float:
        """
        프롬프트 복잡도 계산

        Args:
            prompt: 분석할 프롬프트

        Returns:
            복잡도 점수 (0-10)
        """
        score = 0.0

        # 1. 길이 기반 (0-2점)
        length = len(prompt)
        if length < 100:
            score += 0.5
        elif length < 300:
            score += 1.0
        elif length < 600:
            score += 1.5
        else:
            score += 2.0

        # 2. 단계 수 (0-2점)
        steps = len(re.findall(r'(?:step|단계)\s*\d+|^\d+\.|^-\s', prompt, re.IGNORECASE | re.MULTILINE))
        score += min(2.0, steps * 0.4)

        # 3. 도구 사용 (0-2점)
        tool_mentions = len(re.findall(r'(?:tool|function|api|도구|함수)', prompt, re.IGNORECASE))
        score += min(2.0, tool_mentions * 0.5)

        # 4. 조건부 로직 (0-2점)
        conditionals = len(re.findall(r'(?:if|when|unless|만약|경우)', prompt, re.IGNORECASE))
        score += min(2.0, conditionals * 0.4)

        # 5. 제약사항 (0-2점)
        constraints = len(re.findall(r'(?:must|should|constraint|제약|필수)', prompt, re.IGNORECASE))
        score += min(2.0, constraints * 0.4)

        return min(10.0, score)

    def recommend_reasoning_effort(self, complexity: float) -> ReasoningEffort:
        """
        복잡도 기반 reasoning effort 추천

        Args:
            complexity: 복잡도 점수 (0-10)

        Returns:
            추천 reasoning effort
        """
        thresholds = self.patterns['reasoning_effort_mapping']['complexity_thresholds']

        if complexity <= 3:
            return ReasoningEffort.LOW
        elif complexity <= 7:
            return ReasoningEffort.MEDIUM
        else:
            return ReasoningEffort.HIGH

    def recommend_verbosity(self, prompt: str, complexity: float) -> Verbosity:
        """
        프롬프트 특성 기반 verbosity 추천

        Args:
            prompt: 분석할 프롬프트
            complexity: 복잡도 점수

        Returns:
            추천 verbosity
        """
        # 간결함 요청 키워드
        concise_keywords = ['brief', 'concise', 'short', 'quick', '간단히', '간결하게']
        if any(keyword in prompt.lower() for keyword in concise_keywords):
            return Verbosity.LOW

        # 상세함 요청 키워드
        detailed_keywords = ['detailed', 'comprehensive', 'thorough', 'explain', '상세히', '자세히']
        if any(keyword in prompt.lower() for keyword in detailed_keywords):
            return Verbosity.HIGH

        # 복잡도 기반
        if complexity < 4:
            return Verbosity.LOW
        elif complexity < 7:
            return Verbosity.MEDIUM
        else:
            return Verbosity.HIGH

    def is_xml_structured(self, prompt: str) -> bool:
        """
        XML 구조 사용 여부 확인

        Args:
            prompt: 분석할 프롬프트

        Returns:
            XML 구조 사용 여부
        """
        # 최소 2개 이상의 XML 태그 쌍이 있어야 함
        opening_tags = re.findall(r'<(\w+)>', prompt)
        closing_tags = re.findall(r'</(\w+)>', prompt)

        return len(opening_tags) >= 2 and len(closing_tags) >= 2

    def analyze(self, prompt: str) -> GPT5AnalysisResult:
        """
        전체 분석 수행

        Args:
            prompt: 분석할 프롬프트

        Returns:
            GPT-5 분석 결과
        """
        # 1. 모순 탐지
        contradictions = self.detect_contradictions(prompt)

        # 2. 각 영역 분석
        agentic_score, agentic_suggestions = self.analyze_agentic_structure(prompt)
        clarity_score, clarity_suggestions = self.analyze_clarity(prompt)
        context_score, context_suggestions = self.analyze_context_efficiency(prompt)
        tool_preamble_score, tool_suggestions = self.analyze_tool_preamble(prompt)

        # 3. 복잡도 계산
        complexity = self.calculate_complexity(prompt)

        # 4. 파라미터 추천
        reasoning_effort = self.recommend_reasoning_effort(complexity)
        verbosity = self.recommend_verbosity(prompt, complexity)

        # 5. XML 구조 확인
        xml_structured = self.is_xml_structured(prompt)

        # 6. 이슈 및 제안 통합
        issues = []
        all_suggestions = []

        if contradictions:
            for contradiction in contradictions:
                issues.append({
                    'type': 'contradiction',
                    'severity': contradiction.severity,
                    'description': contradiction.description,
                    'fix': contradiction.fix_strategy
                })

        if agentic_score < 6:
            issues.append({
                'type': 'agentic_structure',
                'severity': 'medium',
                'description': f'Agentic 구조 점수가 낮습니다 ({agentic_score:.1f}/10)',
                'fix': 'Agentic 패턴을 추가하세요'
            })

        if clarity_score < 6:
            issues.append({
                'type': 'clarity',
                'severity': 'medium',
                'description': f'명확성 점수가 낮습니다 ({clarity_score:.1f}/10)',
                'fix': 'XML 구조나 명확한 섹션 구분을 추가하세요'
            })

        if context_score < 6:
            issues.append({
                'type': 'context_efficiency',
                'severity': 'low',
                'description': f'컨텍스트 효율성이 낮습니다 ({context_score:.1f}/10)',
                'fix': '균형잡힌 컨텍스트 수집 지시를 사용하세요'
            })

        # 모든 제안 통합
        all_suggestions.extend(agentic_suggestions)
        all_suggestions.extend(clarity_suggestions)
        all_suggestions.extend(context_suggestions)
        all_suggestions.extend(tool_suggestions)

        return GPT5AnalysisResult(
            original_prompt=prompt,
            contradictions=contradictions,
            agentic_score=agentic_score,
            clarity_score=clarity_score,
            context_efficiency_score=context_score,
            tool_preamble_quality=tool_preamble_score,
            reasoning_effort_recommendation=reasoning_effort.value,
            verbosity_recommendation=verbosity.value,
            xml_structured=xml_structured,
            issues=issues,
            suggestions=all_suggestions,
            complexity_score=complexity
        )


def format_analysis_result(result: GPT5AnalysisResult) -> str:
    """
    분석 결과를 읽기 쉬운 형식으로 포맷팅

    Args:
        result: GPT-5 분석 결과

    Returns:
        포맷팅된 결과 문자열
    """
    output = []

    output.append("=" * 80)
    output.append("GPT-5 프롬프트 분석 결과")
    output.append("=" * 80)
    output.append("")

    # 원본 프롬프트
    output.append("📝 원본 프롬프트:")
    output.append("-" * 80)
    output.append(result.original_prompt[:200] + "..." if len(result.original_prompt) > 200 else result.original_prompt)
    output.append("")

    # 점수
    output.append("📊 분석 점수:")
    output.append(f"  • Agentic 구조: {result.agentic_score:.1f}/10")
    output.append(f"  • 명확성: {result.clarity_score:.1f}/10")
    output.append(f"  • 컨텍스트 효율성: {result.context_efficiency_score:.1f}/10")
    output.append(f"  • 도구 프리앰블 품질: {result.tool_preamble_quality:.1f}/10")
    output.append(f"  • 복잡도: {result.complexity_score:.1f}/10")
    output.append("")

    # 파라미터 추천
    output.append("🎯 추천 파라미터:")
    output.append(f"  • reasoning_effort: {result.reasoning_effort_recommendation}")
    output.append(f"  • verbosity: {result.verbosity_recommendation}")
    output.append(f"  • XML 구조 사용: {'예' if result.xml_structured else '아니오'}")
    output.append("")

    # 모순
    if result.contradictions:
        output.append("⚠️  감지된 모순:")
        for i, contradiction in enumerate(result.contradictions, 1):
            output.append(f"  {i}. {contradiction.description}")
            output.append(f"     심각도: {contradiction.severity}")
            output.append(f"     수정 전략: {contradiction.fix_strategy}")
            output.append("")

    # 이슈
    if result.issues:
        output.append("🔍 발견된 이슈:")
        for i, issue in enumerate(result.issues, 1):
            output.append(f"  {i}. [{issue['severity'].upper()}] {issue['description']}")
            output.append(f"     해결방법: {issue['fix']}")
            output.append("")

    # 제안
    if result.suggestions:
        output.append("💡 개선 제안:")
        for i, suggestion in enumerate(result.suggestions, 1):
            output.append(f"  {i}. {suggestion}")
        output.append("")

    output.append("=" * 80)

    return "\n".join(output)


if __name__ == "__main__":
    # 테스트
    analyzer = GPT5PromptAnalyzer()

    test_prompt = """
    Never proceed without user confirmation but also auto-schedule appointments immediately.
    Maximize context gathering and read all possible files.
    """

    result = analyzer.analyze(test_prompt)
    print(format_analysis_result(result))
