"""
Claude Prompt Optimizer Scripts
프롬프트 최적화 핵심 스크립트 모듈
"""

# Claude 4 최적화 (기존)
from .core import ClaudePromptOptimizer, get_optimizer, optimize_prompt, analyze_prompt
from .analyzer import PromptAnalyzer, AnalysisResult, Domain, OptimizationLevel
from .optimizer import PromptOptimizer, OptimizationResult
from .templates import TemplateManager, Template

# GPT-5 최적화 (신규)
from .gpt5_analyzer import GPT5PromptAnalyzer, GPT5AnalysisResult, ReasoningEffort, Verbosity
from .gpt5_optimizer import GPT5PromptOptimizer, GPT5OptimizationResult
from .gpt5_core import (
    GPT5Engine,
    GPT5PipelineResult,
    analyze_prompt as analyze_gpt5_prompt,
    optimize_prompt as optimize_gpt5_prompt,
    analyze_and_optimize_prompt as analyze_and_optimize_gpt5_prompt
)

__version__ = "1.2.0"
__author__ = "zerodice0"
__description__ = "Claude 4 + GPT-5 프롬프트 최적화 스킬"

# 메인 클래스와 간편 함수들을 외부로 노출
__all__ = [
    # Claude 4 클래스
    "ClaudePromptOptimizer",
    "PromptAnalyzer",
    "PromptOptimizer",
    "TemplateManager",

    # GPT-5 클래스
    "GPT5Engine",
    "GPT5PromptAnalyzer",
    "GPT5PromptOptimizer",

    # Claude 4 데이터 클래스
    "AnalysisResult",
    "OptimizationResult",
    "Template",

    # GPT-5 데이터 클래스
    "GPT5AnalysisResult",
    "GPT5OptimizationResult",
    "GPT5PipelineResult",

    # Claude 4 열거형
    "Domain",
    "OptimizationLevel",

    # GPT-5 열거형
    "ReasoningEffort",
    "Verbosity",

    # Claude 4 간편 함수
    "get_optimizer",
    "optimize_prompt",
    "analyze_prompt",

    # GPT-5 간편 함수
    "analyze_gpt5_prompt",
    "optimize_gpt5_prompt",
    "analyze_and_optimize_gpt5_prompt"
]

# 모듈 정보
def get_version():
    """버전 정보 반환"""
    return __version__

def get_module_info():
    """모듈 정보 반환"""
    return {
        "name": "claude-prompt-optimizer",
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "components": {
            "claude4": [
                "Analyzer: Claude 4 원칙 기반 프롬프트 분석",
                "Optimizer: 토큰 효율성 최적화",
                "Template Manager: 도메인별 템플릿 관리",
                "Core Engine: 통합 최적화 엔진"
            ],
            "gpt5": [
                "GPT5 Analyzer: 모순 탐지, Agentic 구조 평가",
                "GPT5 Optimizer: XML 구조화, 도구 프리앰블, Anti-pattern 수정",
                "GPT5 Engine: 분석 + 최적화 통합 파이프라인",
                "Parameter Recommendations: reasoning_effort, verbosity 자동 추천"
            ]
        }
    }