# 📦 SUMÁRIO DE VERSIONAMENTO - v1.0.3

## Versão Liberada
- **Versão**: 1.0.3
- **Data**: 1 de Junho de 2026
- **Status**: ✅ Liberado no Git

## Mudanças Incluídas

### ✨ Correções Implementadas:
1. **Parser de Volumes** - Corrigida extração quando variação vem no formato "COR,TAMANHO"
   - Ex: "BRANCO NEVE,18L" → Cor: "Branco Neve", Volume: "18L"
   
2. **Detecção de Ambiguidade** - Nova função `count_volumes_in_text()`
   - Identifica títulos com múltiplos tamanhos (ex: "18L 10L 3,6L")
   - Marca como "pending" para classificação manual quando necessário

3. **Lógica de Validação** - Ajustada para não marcar como pendente
   - Quando a variação especifica claramente o tamanho

## Arquivos Modificados
- ✅ `app/core/parser.py` - Adicionada função `count_volumes_in_text()`
- ✅ `app/core/engine.py` - Ajustada lógica de processamento
- ✅ `app/version.py` - Atualizada para v1.0.3
- ✅ `CHANGELOG.md` - Criado arquivo de histórico de versões

## Commit Git
```
Commit: 0887dd5
Mensagem: v1.0.3: Correção de parsing de volumes e detecção de ambiguidade
```

## Tag Git
```
Tag: v1.0.3
Descrição: Release v1.0.3 - Correção de parsing de volumes com formato COR,TAMANHO
```

## Status no Git
- ✅ Push para master - OK
- ✅ Push de tag - OK
- ✅ Sincronizado com origin/master

## Histórico de Versões
```
v1.0.3 - Correção de parsing (NOVA)
v1.0.1 - Versão anterior
v1.0.0 - Versão inicial
```

## Próximos Passos
A versão está pronta para:
- 🚀 Deploy em produção
- 📦 Build do instalador
- 🎉 Release para usuários finais

---
**Gerador de Lista de Produção v1.0.3**
Liberado com sucesso em: 1 de Junho de 2026
