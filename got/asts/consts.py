try:
    from got.asts import utils
except ImportError:
    import utils


class _TraversalOrder(utils.ImmutableMixin, utils.EnumMixin):
    DEPTH_FIRST_PRE_ORDER = "depth-first|pre-order"
    DEPTH_FIRST_POST_ORDER = "depth-first|post-order"
    BREADTH_FIRST = "breadth-first"


class _ASTAlgorithm(utils.ImmutableMixin, utils.EnumMixin):
    EASA = "easa"


class _String(utils.ImmutableMixin, utils.EnumMixin):
    UNICODE_SPECIAL_SYMBOLS_START = 0x0A00

    
ASTAlgorithm = _ASTAlgorithm()
String = _String()
TraversalOrder = _TraversalOrder()
