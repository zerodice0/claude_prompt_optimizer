"""
GPT-5 Prompt Optimizer
GPT-5 특화 프롬프트 최적화기

GPT-5 prompting guide 기반으로 프롬프트를 최적화합니다:
- 모순 제거
- XML 구조화
- 도구 프리앰블 추가
- Agentic 패턴 적용
- 파라미터 설정
"""

import re
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path

from .gpt5_analyzer import GPT5AnalysisResult, Contradiction


@dataclass
class GPT5OptimizationResult:
    """GPT-5 최적화 결과"""
    original_prompt: str
    optimized_prompt: str
    xml_structured_prompt: str
    reasoning_effort: str
    verbosity: str
    improvements: List[str]
    parameter_config: Dict[str, str]
    removed_contradictions: int
    added_features: List[str]

    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return asdict(self)


class GPT5PromptOptimizer:
    """GPT-5 전용 최적화기"""

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

    def remove_contradictions(self, prompt: str, contradictions: List[Contradiction]) -> tuple[str, List[str]]:
        """
        모순 제거 및 통합

        Args:
            prompt: 원본 프롬프트
            contradictions: 감지된 모순 리스트

        Returns:
            (수정된 프롬프트, 적용된 수정사항)
        """
        modified_prompt = prompt
        fixes = []

        for contradiction in contradictions:
            # 모순 패턴별 수정 전략 적용
            if "never.*without" in contradiction.pattern and "auto.*without" in contradiction.pattern:
                # 우선순위 명시로 수정
                modified_prompt = self._fix_permission_contradiction(modified_prompt)
                fixes.append(f"모순 제거: {contradiction.description} → 우선순위 명시")

            elif "always confirm" in contradiction.pattern and "proceed without" in contradiction.pattern:
                # 조건부 로직으로 수정
                modified_prompt = self._fix_confirmation_contradiction(modified_prompt)
                fixes.append(f"모순 제거: {contradiction.description} → 조건부 확인 로직")

            elif "thoroughly" in contradiction.pattern or "maximize" in contradiction.pattern:
                # 균형잡힌 표현으로 수정
                modified_prompt = self._fix_thoroughness_contradiction(modified_prompt)
                fixes.append(f"모순 제거: {contradiction.description} → 균형잡힌 접근")

        return modified_prompt, fixes

    def _fix_permission_contradiction(self, prompt: str) -> str:
        """권한 관련 모순 수정"""
        # "never without" 패턴을 조건부 로직으로 변경
        prompt = re.sub(
            r'never\s+(\w+)\s+without\s+(\w+)',
            r'Only \1 after obtaining \2, except in emergency situations',
            prompt,
            flags=re.IGNORECASE
        )
        return prompt

    def _fix_confirmation_contradiction(self, prompt: str) -> str:
        """확인 관련 모순 수정"""
        # "always confirm" 패턴을 조건부로 변경
        prompt = re.sub(
            r'always\s+confirm',
            r'Confirm for critical actions; proceed automatically for routine tasks',
            prompt,
            flags=re.IGNORECASE
        )
        return prompt

    def _fix_thoroughness_contradiction(self, prompt: str) -> str:
        """철저함 관련 모순 수정"""
        # "maximize" 또는 "thoroughly"를 균형잡힌 표현으로 변경
        prompt = re.sub(
            r'maximize\s+context|gather\s+all\s+possible',
            r'Gather sufficient and relevant context',
            prompt,
            flags=re.IGNORECASE
        )
        prompt = re.sub(
            r'thoroughly\s+(\w+)\s+all',
            r'Efficiently \1 relevant',
            prompt,
            flags=re.IGNORECASE
        )
        return prompt

    def apply_xml_structure(self, prompt: str, analysis: GPT5AnalysisResult) -> tuple[str, List[str]]:
        """
        XML 구조 적용

        Args:
            prompt: 원본 프롬프트
            analysis: 분석 결과

        Returns:
            (XML 구조화된 프롬프트, 적용된 개선사항)
        """
        improvements = []

        # 이미 XML 구조가 있으면 개선, 없으면 생성
        if analysis.xml_structured:
            # 기존 XML 구조 개선
            xml_prompt = prompt
            improvements.append("기존 XML 구조 유지 및 개선")
        else:
            # 새로운 XML 구조 생성
            xml_prompt = self._create_xml_structure(prompt, analysis)
            improvements.append("XML 구조 생성")

        return xml_prompt, improvements

    def _create_xml_structure(self, prompt: str, analysis: GPT5AnalysisResult) -> str:
        """새로운 XML 구조 생성"""
        # 프롬프트 복잡도에 따라 템플릿 선택
        if analysis.complexity_score >= 7:
            template_name = "agentic"
        elif analysis.agentic_score >= 6:
            template_name = "agentic"
        else:
            template_name = "basic"

        template = self.patterns['xml_structures'][template_name]['template']

        # 프롬프트 내용 파싱
        role = self._extract_role(prompt)
        task = self._extract_task(prompt)
        constraints = self._extract_constraints(prompt)

        if template_name == "agentic":
            preambles = self._generate_tool_preambles(analysis)
            persistence = self._generate_persistence(analysis)
            escapes = self._generate_escape_hatches(analysis)

            xml_prompt = template.format(
                preambles=preambles,
                persistence=persistence,
                escapes=escapes,
                constraints=constraints
            )
        else:
            xml_prompt = template.format(
                role=role,
                task=task,
                constraints=constraints
            )

        # 원본 프롬프트 내용 추가
        if not role or not task:
            xml_prompt += f"\n\n<!-- 원본 프롬프트 내용 -->\n{prompt}"

        return xml_prompt

    def _extract_role(self, prompt: str) -> str:
        """프롬프트에서 역할 추출"""
        role_patterns = [
            r'you are (?:a |an )?(\w+(?:\s+\w+)*)',
            r'act as (?:a |an )?(\w+(?:\s+\w+)*)',
            r'role:\s*(\w+(?:\s+\w+)*)'
        ]

        for pattern in role_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                return match.group(1)

        return "AI assistant"

    def _extract_task(self, prompt: str) -> str:
        """프롬프트에서 작업 추출"""
        # 첫 문장 또는 명령문 추출
        sentences = re.split(r'[.!?]\s+', prompt)
        if sentences:
            return sentences[0].strip()
        return prompt[:100]

    def _extract_constraints(self, prompt: str) -> str:
        """프롬프트에서 제약사항 추출"""
        constraint_keywords = ['must', 'should', 'never', 'always', 'constraint', 'requirement']
        constraints = []

        for line in prompt.split('\n'):
            if any(keyword in line.lower() for keyword in constraint_keywords):
                constraints.append(line.strip())

        return '\n'.join(constraints) if constraints else "No specific constraints"

    def _generate_tool_preambles(self, analysis: GPT5AnalysisResult) -> str:
        """도구 프리앰블 생성"""
        preambles = self.patterns['tool_preambles']['user_friendly']['components']
        return '\n'.join(f"- {p}" for p in preambles)

    def _generate_persistence(self, analysis: GPT5AnalysisResult) -> str:
        """지속성 지시 생성"""
        if analysis.complexity_score >= 7:
            pattern = self.patterns['agentic_patterns']['high_eagerness']['characteristics']
            return '\n'.join(f"- {p}" for p in pattern)
        else:
            pattern = self.patterns['agentic_patterns']['medium_eagerness']['characteristics']
            return '\n'.join(f"- {p}" for p in pattern)

    def _generate_escape_hatches(self, analysis: GPT5AnalysisResult) -> str:
        """Escape hatch 생성"""
        return "If 70% confident in the solution, proceed with best judgment and document assumptions."

    def add_tool_preambles(self, prompt: str, analysis: GPT5AnalysisResult) -> tuple[str, List[str]]:
        """
        도구 프리앰블 추가

        Args:
            prompt: 원본 프롬프트
            analysis: 분석 결과

        Returns:
            (프리앰블이 추가된 프롬프트, 적용된 개선사항)
        """
        improvements = []

        # 도구 프리앰블이 이미 있는지 확인
        if analysis.tool_preamble_quality >= 7:
            return prompt, ["기존 도구 프리앰블 충분"]

        # 프리앰블 추가
        preamble_section = "\n\n## Tool Usage Guidelines\n\n"

        components = self.patterns['tool_preambles']['user_friendly']['components']
        for component in components:
            preamble_section += f"- {component}\n"

        # 예시 추가
        preamble_section += "\n### Example:\n"
        for example in self.patterns['tool_preambles']['user_friendly']['examples']:
            preamble_section += f"- {example}\n"

        enhanced_prompt = prompt + preamble_section
        improvements.append("도구 프리앰블 추가 (목표 재구성, 계획, 진행 상황 업데이트)")

        return enhanced_prompt, improvements

    def apply_agentic_patterns(self, prompt: str, analysis: GPT5AnalysisResult) -> tuple[str, List[str]]:
        """
        Agentic 패턴 적용

        Args:
            prompt: 원본 프롬프트
            analysis: 분석 결과

        Returns:
            (Agentic 패턴이 적용된 프롬프트, 적용된 개선사항)
        """
        improvements = []

        # Eagerness 레벨 결정
        if analysis.complexity_score >= 7:
            eagerness = "high_eagerness"
        elif analysis.complexity_score >= 4:
            eagerness = "medium_eagerness"
        else:
            eagerness = "low_eagerness"

        pattern = self.patterns['agentic_patterns'][eagerness]

        # Agentic 섹션 추가
        agentic_section = f"\n\n## Agentic Behavior ({pattern['description']})\n\n"

        for prompt_pattern in pattern['prompt_patterns']:
            agentic_section += f"- {prompt_pattern}\n"

        enhanced_prompt = prompt + agentic_section
        improvements.append(f"Agentic 패턴 적용: {eagerness} ({pattern['description']})")

        return enhanced_prompt, improvements

    def optimize_verbosity(self, prompt: str, analysis: GPT5AnalysisResult) -> tuple[str, List[str]]:
        """
        Verbosity 최적화

        Args:
            prompt: 원본 프롬프트
            analysis: 분석 결과

        Returns:
            (Verbosity가 최적화된 프롬프트, 적용된 개선사항)
        """
        improvements = []

        verbosity_instruction = f"\n\n## Response Style\n\n"

        if analysis.verbosity_recommendation == "low":
            verbosity_instruction += "- Be concise and direct\n"
            verbosity_instruction += "- Focus on essential information only\n"
            verbosity_instruction += "- Avoid unnecessary explanations\n"
            improvements.append("Verbosity 최적화: 간결한 응답")

        elif analysis.verbosity_recommendation == "high":
            verbosity_instruction += "- Provide detailed explanations\n"
            verbosity_instruction += "- Include examples and alternatives\n"
            verbosity_instruction += "- Explain reasoning and background\n"
            improvements.append("Verbosity 최적화: 상세한 응답")

        else:
            verbosity_instruction += "- Provide balanced explanations\n"
            verbosity_instruction += "- Include context where helpful\n"
            improvements.append("Verbosity 최적화: 균형잡힌 응답")

        enhanced_prompt = prompt + verbosity_instruction

        return enhanced_prompt, improvements

    def fix_anti_patterns(self, prompt: str) -> tuple[str, List[str]]:
        """
        Anti-pattern 수정

        Args:
            prompt: 원본 프롬프트

        Returns:
            (Anti-pattern이 수정된 프롬프트, 적용된 개선사항)
        """
        modified_prompt = prompt
        fixes = []

        # 1. 과도한 철저함 강조 제거
        anti_pattern = self.patterns['anti_patterns']['over_emphasis_thoroughness']
        for example in anti_pattern['examples']:
            if example.lower() in modified_prompt.lower():
                # 균형잡힌 표현으로 교체
                modified_prompt = re.sub(
                    re.escape(example),
                    "Gather sufficient and relevant information",
                    modified_prompt,
                    flags=re.IGNORECASE
                )
                fixes.append(f"Anti-pattern 수정: {anti_pattern['description']}")

        # 2. Escape hatch 추가
        anti_pattern = self.patterns['anti_patterns']['missing_escape_hatches']
        for example in anti_pattern['examples']:
            if example.lower() in modified_prompt.lower():
                # 임계값 추가
                modified_prompt = re.sub(
                    re.escape(example),
                    "If 70% confident, proceed with best judgment",
                    modified_prompt,
                    flags=re.IGNORECASE
                )
                fixes.append(f"Anti-pattern 수정: {anti_pattern['description']}")

        # 3. 명확한 도구 정의
        anti_pattern = self.patterns['anti_patterns']['ambiguous_tool_definitions']
        for example in anti_pattern['examples']:
            if example.lower() in modified_prompt.lower():
                # 구체적인 기준 추가
                modified_prompt = re.sub(
                    re.escape(example),
                    "Use tools when: 1) Information is missing, 2) Action is required, 3) Validation is needed",
                    modified_prompt,
                    flags=re.IGNORECASE
                )
                fixes.append(f"Anti-pattern 수정: {anti_pattern['description']}")

        return modified_prompt, fixes

    def optimize(self, analysis: GPT5AnalysisResult) -> GPT5OptimizationResult:
        """
        전체 최적화 수행

        Args:
            analysis: GPT-5 분석 결과

        Returns:
            GPT-5 최적화 결과
        """
        prompt = analysis.original_prompt
        all_improvements = []
        added_features = []

        # 1. 모순 제거
        if analysis.contradictions:
            prompt, fixes = self.remove_contradictions(prompt, analysis.contradictions)
            all_improvements.extend(fixes)
            added_features.append("모순 제거 및 통합")

        # 2. Anti-pattern 수정
        prompt, fixes = self.fix_anti_patterns(prompt)
        if fixes:
            all_improvements.extend(fixes)
            added_features.append("Anti-pattern 수정")

        # 3. 도구 프리앰블 추가
        if analysis.tool_preamble_quality < 7:
            prompt, improvements = self.add_tool_preambles(prompt, analysis)
            all_improvements.extend(improvements)
            if improvements:
                added_features.append("도구 프리앰블")

        # 4. Agentic 패턴 적용
        if analysis.agentic_score < 7:
            prompt, improvements = self.apply_agentic_patterns(prompt, analysis)
            all_improvements.extend(improvements)
            if improvements:
                added_features.append("Agentic 패턴")

        # 5. Verbosity 최적화
        prompt, improvements = self.optimize_verbosity(prompt, analysis)
        all_improvements.extend(improvements)
        added_features.append("Verbosity 최적화")

        # 6. XML 구조 생성 (최종)
        xml_prompt, improvements = self.apply_xml_structure(prompt, analysis)
        if improvements:
            all_improvements.extend(improvements)
            added_features.append("XML 구조화")

        # 파라미터 설정
        parameter_config = {
            "reasoning_effort": analysis.reasoning_effort_recommendation,
            "verbosity": analysis.verbosity_recommendation,
            "model": "gpt-5" if analysis.complexity_score >= 7 else "gpt-4"
        }

        return GPT5OptimizationResult(
            original_prompt=analysis.original_prompt,
            optimized_prompt=prompt,
            xml_structured_prompt=xml_prompt,
            reasoning_effort=analysis.reasoning_effort_recommendation,
            verbosity=analysis.verbosity_recommendation,
            improvements=all_improvements,
            parameter_config=parameter_config,
            removed_contradictions=len(analysis.contradictions),
            added_features=added_features
        )


def format_optimization_result(result: GPT5OptimizationResult) -> str:
    """
    최적화 결과를 읽기 쉬운 형식으로 포맷팅

    Args:
        result: GPT-5 최적화 결과

    Returns:
        포맷팅된 결과 문자열
    """
    output = []

    output.append("=" * 80)
    output.append("GPT-5 프롬프트 최적화 결과")
    output.append("=" * 80)
    output.append("")

    # 원본 프롬프트
    output.append("📝 원본 프롬프트:")
    output.append("-" * 80)
    output.append(result.original_prompt[:200] + "..." if len(result.original_prompt) > 200 else result.original_prompt)
    output.append("")

    # 최적화된 프롬프트
    output.append("✅ 최적화된 프롬프트:")
    output.append("-" * 80)
    output.append(result.optimized_prompt[:300] + "..." if len(result.optimized_prompt) > 300 else result.optimized_prompt)
    output.append("")

    # 파라미터 설정
    output.append("🎯 권장 파라미터:")
    for key, value in result.parameter_config.items():
        output.append(f"  • {key}: {value}")
    output.append("")

    # 적용된 개선사항
    output.append("🔧 적용된 개선사항:")
    for i, improvement in enumerate(result.improvements, 1):
        output.append(f"  {i}. {improvement}")
    output.append("")

    # 추가된 기능
    if result.added_features:
        output.append("✨ 추가된 기능:")
        for feature in result.added_features:
            output.append(f"  • {feature}")
        output.append("")

    # 통계
    output.append("📊 최적화 통계:")
    output.append(f"  • 제거된 모순: {result.removed_contradictions}개")
    output.append(f"  • 적용된 개선: {len(result.improvements)}개")
    output.append(f"  • 추가된 기능: {len(result.added_features)}개")
    output.append("")

    # XML 구조화된 버전
    output.append("📋 XML 구조화 버전:")
    output.append("-" * 80)
    output.append(result.xml_structured_prompt[:400] + "..." if len(result.xml_structured_prompt) > 400 else result.xml_structured_prompt)
    output.append("")

    output.append("=" * 80)

    return "\n".join(output)


if __name__ == "__main__":
    # 테스트
    from .gpt5_analyzer import GPT5PromptAnalyzer

    analyzer = GPT5PromptAnalyzer()
    optimizer = GPT5PromptOptimizer()

    test_prompt = """
    Never proceed without user confirmation but also auto-schedule appointments immediately.
    Maximize context gathering and read all possible files.
    """

    # 분석
    analysis = analyzer.analyze(test_prompt)

    # 최적화
    result = optimizer.optimize(analysis)

    print(format_optimization_result(result))
