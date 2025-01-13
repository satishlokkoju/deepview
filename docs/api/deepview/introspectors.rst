=================
Introspectors API
=================

.. contents:: Contents
    :local:


Data Introspectors
-------------------
Familiarity
~~~~~~~~~~~
.. autoclass:: deepview.introspectors.Familiarity
    :members:

.. autoclass:: deepview.introspectors.FamiliarityStrategyType
    :members:
    :special-members: __call__

.. autoclass:: deepview.introspectors.FamiliarityResult
    :members:

.. autoclass:: deepview.introspectors.GMMCovarianceType
    :members:

.. autoclass:: deepview.introspectors.FamiliarityDistribution
    :members: compute_familiarity_score

Dimensionality Reduction
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: deepview.introspectors.DimensionReduction
    :members:
    :exclude-members: check_batch_size, default_batch_size, fit_complete, fit_incremental,
        is_one_shot, transform, transform_one_shot

.. py:data:: OneOrManyDimStrategies

alias of Union[DimensionReductionStrategyType, Mapping[str, DimensionReductionStrategyType]]

.. autoclass:: deepview.introspectors.DimensionReductionStrategyType
    :members:

Duplicates
~~~~~~~~~~

.. autoclass:: deepview.introspectors.Duplicates
    :members: KNNStrategy, ThresholdStrategy, DuplicateSetCandidate, introspect, results, count
    :undoc-members:

.. autoclass:: deepview.introspectors.DuplicatesStrategyType
    :special-members: __call__

.. autoclass:: deepview.introspectors.DuplicatesThresholdStrategyType
    :special-members: __call__


Dataset Report
~~~~~~~~~~~~~~

.. autoclass:: deepview.introspectors.DatasetReport
    :members:

.. autoclass:: deepview.introspectors.ReportConfig
    :members:


Model Introspectors
-------------------

Principal Filter Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: deepview.introspectors.PFA
    :members:

.. autoclass:: deepview.introspectors.PFAKLDiagnostics
    :members:

.. autoclass:: deepview.introspectors.PFAEnergyDiagnostics
    :members:

.. autoclass:: deepview.introspectors.PFARecipe
    :members:

.. autoclass:: deepview.introspectors.PFAUnitSelectionStrategyType
    :special-members: __call__

.. autoclass:: deepview.introspectors.PFAStrategyType
    :special-members: __call__

.. autoclass:: deepview.introspectors.PFACovariancesResult
    :members:

Inactive Unit Analysis
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: deepview.introspectors.IUA
    :members:
