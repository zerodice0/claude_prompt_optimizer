"""
Claude Prompt Optimizer Scripts
프롬프트 최적화 핵심 스크립트 모듈
"""

from .core import ClaudePromptOptimizer, get_optimizer, optimize_prompt, analyze_prompt
from .analyzer import PromptAnalyzer, AnalysisResult, Domain, OptimizationLevel
from .optimizer import PromptOptimizer, OptimizationResult
from .templates import TemplateManager, Template

__version__ = "1.0.0"
__author__ = "zerodice0"
__description__ = "Claude 4 기반 프롬프트 최적화 스킬"

# 메인 클래스와 간편 함수들을 외부로 노출
__all__ = [
    # 메인 클래스
    "ClaudePromptOptimizer",
    "PromptAnalyzer",
    "PromptOptimizer",
    "TemplateManager",

    # 데이터 클래스
    "AnalysisResult",
    "OptimizationResult",
    "Template",

    # 열거형
    "Domain",
    "OptimizationLevel",

    # 간편 함수
    "get_optimizer",
    "optimize_prompt",
    "analyze_prompt"
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
        "components": [
            "Analyzer: Claude 4 원칙 기반 프롬프트 분석",
            "Optimizer: 토큰 효율성 최적화",
            "Template Manager: 도메인별 템플릿 관리",
            "Core Engine: 통합 최적화 엔진"
        ]
    }