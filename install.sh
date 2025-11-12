#!/bin/bash

# Claude Prompt Optimizer 설치 스크립트
# 작성자: zerodice0
# 버전: 1.1.0

set -e # 에러 발생 시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로고 출력
echo -e "${BLUE}"
cat <<"EOF"
╔═══════════════════════════════════════════════════════╗
║   Claude Prompt Optimizer                            ║
║   7원칙 기반 프롬프트 최적화 도구                      ║
║   v1.0.1                                             ║
╚═══════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# 설치 옵션 확인
echo -e "${YELLOW}설치 방법을 선택하세요:${NC}"
echo "1) Claude Code 프로젝트 (현재 디렉토리)"
echo "2) Claude Skills (~/.claude/skills)"
echo "3) 취소"
echo ""
read -p "선택 (1-3): " choice

case $choice in
1)
  INSTALL_DIR="$(pwd)/claude_prompt_optimizer"
  INSTALL_TYPE="project"
  ;;
2)
  INSTALL_DIR="$HOME/.claude/skills/prompt-optimizer"
  INSTALL_TYPE="skills"
  ;;
3)
  echo -e "${YELLOW}설치를 취소했습니다.${NC}"
  exit 0
  ;;
*)
  echo -e "${RED}잘못된 선택입니다.${NC}"
  exit 1
  ;;
esac

echo -e "${BLUE}설치 위치: ${INSTALL_DIR}${NC}"

# 디렉토리 존재 확인
if [ -d "$INSTALL_DIR" ]; then
  echo -e "${YELLOW}경고: 디렉토리가 이미 존재합니다.${NC}"
  read -p "덮어쓰시겠습니까? (y/n): " overwrite
  if [ "$overwrite" != "y" ]; then
    echo -e "${YELLOW}설치를 취소했습니다.${NC}"
    exit 0
  fi
  rm -rf "$INSTALL_DIR"
fi

# Git 설치 확인
if ! command -v git &>/dev/null; then
  echo -e "${RED}에러: Git이 설치되어 있지 않습니다.${NC}"
  echo "Git을 먼저 설치해주세요: https://git-scm.com/"
  exit 1
fi

# Python 설치 확인
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}에러: Python 3가 설치되어 있지 않습니다.${NC}"
  echo "Python 3.8 이상을 설치해주세요: https://www.python.org/"
  exit 1
fi

# Python 버전 확인
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
  echo -e "${RED}에러: Python 3.8 이상이 필요합니다. (현재: $PYTHON_VERSION)${NC}"
  exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION 확인됨${NC}"

# 저장소 클론
echo -e "${BLUE}저장소를 클론하는 중...${NC}"
if [ "$INSTALL_TYPE" = "skills" ]; then
  mkdir -p "$HOME/.claude/skills"
fi

git clone https://github.com/zerodice0/claude_prompt_optimizer.git "$INSTALL_DIR"

if [ $? -ne 0 ]; then
  echo -e "${RED}에러: 저장소 클론에 실패했습니다.${NC}"
  exit 1
fi

echo -e "${GREEN}✓ 저장소 클론 완료${NC}"

# 의존성 설치 (선택사항)
echo ""
read -p "Anthropic Python 패키지를 설치하시겠습니까? (선택사항) (y/n): " install_deps

if [ "$install_deps" = "y" ]; then
  echo -e "${BLUE}의존성을 설치하는 중...${NC}"
  pip3 install anthropic
  echo -e "${GREEN}✓ 의존성 설치 완료${NC}"
fi

# Claude Code 설정 파일 업데이트 (Skills 설치 시)
if [ "$INSTALL_TYPE" = "skills" ]; then
  echo -e "${BLUE}전역 slash commands를 설정하는 중...${NC}"

  # ~/.claude/commands 디렉토리 생성
  COMMANDS_DIR="$HOME/.claude/commands/prompt"
  mkdir -p "$COMMANDS_DIR"

  # analyze-prompt.md 생성
  cat >"$COMMANDS_DIR/analyze-prompt.md" <<'EOF'
# Prompt Analysis

Execute the following Python script to analyze the prompt:

```bash
python3 -c "
import sys
sys.path.insert(0, '$HOME/.claude/skills/prompt-optimizer')
from scripts.core import analyze_prompt

prompt_text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
result = analyze_prompt(prompt_text)

print('\n🔍 프롬프트 분석 결과\n')
print(f'📝 원본: {result[\"original_prompt\"]}\n')
print('📊 7원칙 평가:')
for principle, score in result['scores'].items():
    stars = '⭐' * int(score)
    print(f'  {principle}: {stars} ({score}/5)')
print(f'\n💡 주요 개선 제안:')
for suggestion in result['suggestions']:
    print(f'  • {suggestion}')
print(f'\n⚠️  발견된 문제:')
for issue in result['issues']:
    print(f'  ⚠️  {issue}')
print(f'\n🎯 도메인: {result[\"domain\"]}')
print(f'🎭 의도: {result[\"intent\"]}')
print(f'⚡ 복잡도: {result[\"complexity\"]}')
print(f'📊 총점: {result[\"total_score\"]}/35')
print(f'🔢 토큰 수: {result[\"token_count\"]}')
print(f'\n{result[\"summary\"]}')
" "$@"
```
EOF

  # optimize-prompt.md 생성
  cat >"$COMMANDS_DIR/optimize-prompt.md" <<'EOF'
# Prompt Optimization

Execute the following Python script to optimize the prompt:

```bash
python3 -c "
import sys
sys.path.insert(0, '$HOME/.claude/skills/prompt-optimizer')
from scripts.core import optimize_prompt

prompt_text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
result = optimize_prompt(prompt_text)

print('\n✨ 프롬프트 최적화 결과\n')
print(f'📝 원본: {result[\"original_prompt\"]}\n')
print(f'✅ 최적화: {result[\"optimized_prompt\"]}\n')
print('📊 개선 사항:')
for improvement in result['improvements']:
    print(f'  ✓ {improvement}')
print(f'\n🎯 토큰 효율: {result[\"token_reduction\"]}% 절감')
print(f'📊 원본 토큰: {result[\"original_tokens\"]}')
print(f'📊 최적화 토큰: {result[\"optimized_tokens\"]}')
" "$@"
```
EOF

  echo -e "${GREEN}✓ 전역 slash commands 설정 완료${NC}"
  echo -e "${GREEN}  - /analyze-prompt${NC}"
  echo -e "${GREEN}  - /optimize-prompt${NC}"
fi

# 설치 완료
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   설치 완료!                                         ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}사용 방법:${NC}"
echo ""

if [ "$INSTALL_TYPE" = "project" ]; then
  echo "1. 프로젝트 디렉토리로 이동:"
  echo "   cd $INSTALL_DIR"
  echo ""
fi

echo "2. Slash Commands 사용:"
echo "   /analyze-prompt \"분석할 프롬프트\""
echo "   /optimize-prompt \"최적화할 프롬프트\""
echo ""
echo "3. Python API 직접 사용:"
echo "   from scripts import analyze_prompt, optimize_prompt"
echo "   result = optimize_prompt(\"프롬프트\")"
echo ""
echo -e "${BLUE}문서:${NC}"
echo "   README: $INSTALL_DIR/README.md"
echo "   GitHub: https://github.com/zerodice0/claude_prompt_optimizer"
echo ""
echo -e "${GREEN}즐거운 프롬프트 최적화 되세요! 🚀${NC}"
