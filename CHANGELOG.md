# Changelog

Todas as mudanças notáveis deste projeto estão documentadas neste arquivo.

## [1.0.3] - 2026-06-01

### Fixed
- **Parser de Volumes**: Corrigido o padrão de extração de volumes quando a variação contém "COR,TAMANHO" (ex: "BRANCO NEVE,18L")
- **Detecção de Ambiguidade**: Adicionada função `count_volumes_in_text()` para identificar quando o título tem múltiplos tamanhos disponíveis
- **Lógica de Validação**: Ajustada a lógica de status ("pending" vs "success") para não marcar como pendente quando a variação especifica claramente o tamanho

### Changed
- **Extração de Cores**: Melhorada para remover corretamente o tamanho do formato "COR,TAMANHO"
- **Priorização de Volumes**: Volumes em variações agora são priorizados quando vêm após vírgula

### Technical Details
- Arquivo modificado: `app/core/parser.py` - Adicionada função `count_volumes_in_text()`
- Arquivo modificado: `app/core/engine.py` - Ajustada lógica de processamento em `process_dataframe()`

## [1.0.2] - (Tag desatualizada, ignorar)

## [1.0.1] - 2026-05-XX

### Initial Release
- Aplicação base com funcionalidades de importação de Excel
- Sistema de banco de dados SQLite
- Temas dark/light
- Print de listas
