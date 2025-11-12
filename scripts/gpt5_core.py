"""
GPT-5 Core
GPT-5 프롬프트 분석 및 최적화 통합 엔진

분석과 최적화를 하나의 파이프라인으로 실행하는 통합 API 제공
"""

from typing import Dict, Optional
from dataclasses import dataclass, asdict

from .gpt5_analyzer import GPT5PromptAnalyzer, GPT5AnalysisResult, format_analysis_result
from .gpt5_optimizer import GPT5PromptOptimizer, GPT5OptimizationResult, format_optimization_result


@dataclass
class GPT5PipelineResult:
    """GPT-5 파이프라인 전체 결과"""
    original_prompt: str
    analysis: GPT5AnalysisResult
    optimization: GPT5OptimizationResult

    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'original_prompt': self.original_prompt,
            'analysis': self.analysis.to_dict(),
            'optimization': self.optimization.to_dict()
        }


class GPT5Engine:
    """GPT-5 통합 엔진"""

    def __init__(self, patterns_file: Optional[str] = None):
        """
        초기화

        Args:
            patterns_file: GPT-5 패턴 파일 경로 (None이면 기본 경로 사용)
        """
        self.analyzer = GPT5PromptAnalyzer(patterns_file)
        self.optimizer = GPT5PromptOptimizer(patterns_file)

    def analyze(self, prompt: str) -> GPT5AnalysisResult:
        """
        프롬프트 분석

        Args:
            prompt: 분석할 프롬프트

        Returns:
            GPT-5 분석 결과
        """
        return self.analyzer.analyze(prompt)

    def optimize(self, prompt: str) -> GPT5OptimizationResult:
        """
        프롬프트 최적화 (분석 포함)

        Args:
            prompt: 최적화할 프롬프트

        Returns:
            GPT-5 최적화 결과
        """
        # 먼저 분석
        analysis = self.analyzer.analyze(prompt)

        # 분석 결과로 최적화
        optimization = self.optimizer.optimize(analysis)

        return optimization

    def analyze_and_optimize(self, prompt: str) -> GPT5PipelineResult:
        """
        분석과 최적화 전체 파이프라인 실행

        Args:
            prompt: 분석 및 최적화할 프롬프트

        Returns:
            전체 파이프라인 결과
        """
        # 분석
        analysis = self.analyzer.analyze(prompt)

        # 최적화
        optimization = self.optimizer.optimize(analysis)

        return GPT5PipelineResult(
            original_prompt=prompt,
            analysis=analysis,
            optimization=optimization
        )


def format_pipeline_result(result: GPT5PipelineResult, include_analysis: bool = True) -> str:
    """
    파이프라인 결과를 읽기 쉬운 형식으로 포맷팅

    Args:
        result: GPT-5 파이프라인 결과
        include_analysis: 분석 결과 포함 여부

    Returns:
        포맷팅된 결과 문자열
    """
    output = []

    output.append("=" * 80)
    output.append("GPT-5 프롬프트 분석 및 최적화 결과")
    output.append("=" * 80)
    output.append("")

    # 원본 프롬프트
    output.append("📝 원본 프롬프트:")
    output.append("-" * 80)
    output.append(result.original_prompt)
    output.append("")
    output.append("")

    # 분석 결과 (선택적)
    if include_analysis:
        output.append("=" * 80)
        output.append("1️⃣  분석 단계")
        output.append("=" * 80)
        output.append("")

        # 점수
        analysis = result.analysis
        output.append("📊 분석 점수:")
        output.append(f"  • Agentic 구조: {analysis.agentic_score:.1f}/10")
        output.append(f"  • 명확성: {analysis.clarity_score:.1f}/10")
        output.append(f"  • 컨텍스트 효율성: {analysis.context_efficiency_score:.1f}/10")
        output.append(f"  • 도구 프리앰블 품질: {analysis.tool_preamble_quality:.1f}/10")
        output.append(f"  • 복잡도: {analysis.complexity_score:.1f}/10")
        output.append("")

        # 파라미터 추천
        output.append("🎯 추천 파라미터:")
        output.append(f"  • reasoning_effort: {analysis.reasoning_effort_recommendation}")
        output.append(f"  • verbosity: {analysis.verbosity_recommendation}")
        output.append(f"  • XML 구조 사용: {'예' if analysis.xml_structured else '아니오'}")
        output.append("")

        # 모순
        if analysis.contradictions:
            output.append("⚠️  감지된 모순:")
            for i, contradiction in enumerate(analysis.contradictions, 1):
                output.append(f"  {i}. {contradiction.description}")
                output.append(f"     심각도: {contradiction.severity}")
                output.append("")

        # 주요 이슈
        if analysis.issues:
            output.append("🔍 주요 이슈:")
            for i, issue in enumerate(analysis.issues[:3], 1):  # 상위 3개만
                output.append(f"  {i}. [{issue['severity'].upper()}] {issue['description']}")
                output.append("")

        output.append("")

    # 최적화 결과
    output.append("=" * 80)
    output.append("2️⃣  최적화 단계")
    output.append("=" * 80)
    output.append("")

    optimization = result.optimization

    # 적용된 개선사항
    output.append("🔧 적용된 개선사항:")
    for i, improvement in enumerate(optimization.improvements, 1):
        output.append(f"  {i}. {improvement}")
    output.append("")

    # 추가된 기능
    if optimization.added_features:
        output.append("✨ 추가된 기능:")
        for feature in optimization.added_features:
            output.append(f"  • {feature}")
        output.append("")

    # 최적화 통계
    output.append("📊 최적화 통계:")
    output.append(f"  • 제거된 모순: {optimization.removed_contradictions}개")
    output.append(f"  • 적용된 개선: {len(optimization.improvements)}개")
    output.append(f"  • 추가된 기능: {len(optimization.added_features)}개")
    output.append("")

    # 최적화된 프롬프트
    output.append("=" * 80)
    output.append("3️⃣  최종 결과")
    output.append("=" * 80)
    output.append("")

    output.append("✅ 최적화된 프롬프트:")
    output.append("-" * 80)
    output.append(optimization.optimized_prompt)
    output.append("")
    output.append("")

    # 파라미터 설정
    output.append("🎯 권장 실행 파라미터:")
    output.append("-" * 80)
    for key, value in optimization.parameter_config.items():
        output.append(f"{key}: {value}")
    output.append("")
    output.append("")

    # XML 구조화 버전
    output.append("📋 XML 구조화 버전:")
    output.append("-" * 80)
    output.append(optimization.xml_structured_prompt)
    output.append("")

    output.append("=" * 80)

    return "\n".join(output)


def analyze_prompt(prompt: str, patterns_file: Optional[str] = None) -> str:
    """
    프롬프트 분석 (간편 API)

    Args:
        prompt: 분석할 프롬프트
        patterns_file: 패턴 파일 경로

    Returns:
        포맷팅된 분석 결과
    """
    engine = GPT5Engine(patterns_file)
    result = engine.analyze(prompt)
    return format_analysis_result(result)


def optimize_prompt(prompt: str, patterns_file: Optional[str] = None) -> str:
    """
    프롬프트 최적화 (간편 API)

    Args:
        prompt: 최적화할 프롬프트
        patterns_file: 패턴 파일 경로

    Returns:
        포맷팅된 최적화 결과
    """
    engine = GPT5Engine(patterns_file)
    result = engine.optimize(prompt)
    return format_optimization_result(result)


def analyze_and_optimize_prompt(prompt: str, patterns_file: Optional[str] = None, include_analysis: bool = True) -> str:
    """
    프롬프트 분석 및 최적화 (간편 API)

    Args:
        prompt: 분석 및 최적화할 프롬프트
        patterns_file: 패턴 파일 경로
        include_analysis: 분석 결과 포함 여부

    Returns:
        포맷팅된 전체 결과
    """
    engine = GPT5Engine(patterns_file)
    result = engine.analyze_and_optimize(prompt)
    return format_pipeline_result(result, include_analysis)


# 편의 함수들 export
__all__ = [
    'GPT5Engine',
    'GPT5PipelineResult',
    'analyze_prompt',
    'optimize_prompt',
    'analyze_and_optimize_prompt',
    'format_pipeline_result'
]


if __name__ == "__main__":
    # 테스트
    test_prompt = """
    Create a web application with user authentication.
    Never allow access without proper credentials but also enable automatic guest access.
    Maximize information gathering from all sources.
    """

    print("=" * 80)
    print("GPT-5 엔진 테스트")
    print("=" * 80)
    print("")

    # 전체 파이프라인 실행
    result = analyze_and_optimize_prompt(test_prompt)
    print(result)
