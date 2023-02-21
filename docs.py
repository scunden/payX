WELCOME="""
Welcome to the Talent AI Pay X tool - a completely self serve tool that your organization can use to learn about pay equity, and
run your own pay equity analyses to ensure that you are compliant with OFCCP regulations! The pay equity analysis is divided into a few sections, detailed below.
"""

KEY_VARIABLES="""
In this section, you will be asked to enter all of the key information pertraining to your data and the analysis. This includes 
identifying which legitimate (tenure, job level, etc.) and illegitimate factors (gender, race, etc.) will be included in the analysis
as well as how the analysis is cut in terms of job groups. Click on any of the buttons below to learn more.
"""

JOB_GROUP="""
Job groups, as defined by the OFCCP, are groups of similarly situated employees for which a analysis of pay should be conducted.
Pay gaps, drivers of pay, and outliers are all reported by job group, meaning that you would obtain a pay gap for every job group you create.
In an ideal world, job groups would simply be the same as job titles - since at that level, you would expect employees with the same job title, to do the same work, and be paid the same assuming other criterias such as tenure are comparable.

However, were we to define job groups this way, most organizations would have hundreds if not thousands of job groups, most of which would be only have a handful of employees.
These job groups would be too small for a statistical analysis. There would also be too many results for any organization to properly digest.

This is in part why the OFCCP requires job group to group together employees doing *similar* work, not the same exact work. This allows for larger job groups 
that are big enough for a statistical analysis, while still comparing employees in similar situations.

"""

VALIDATION="""
Once you have selected your key variables and ran the analysis, you can now proceed to the analysis of the results. However, we must first
ensure that certain statistical standards are met and that some key factors are not overlooked.

In this section, you will be able to review the statistical rigor of your analysis, and understand whether some modifications to the data 
are required, and if so, what they are. This section ensures that you can properly disect your pay equity results without having to worry about
whether the results are statistically valid or not. Click on any of the buttons below to learn more.
"""

MINIMUM_HEADCOUNT="""
The OFCCP requires a statistical analysis using regression models to evaluate impact of gender and other discriminatory factors
on pay. In order to run these analyses, there needs to be a balance between the number of employees being analyzed, and the 
number of variables used in the analysis.

In this case, there are simply too few employees in the above job groups for a statistical analysis to be valid.
Please consider further consolidating these smaller job groups into broader, bigger job groups (usually 100 employees is the minimum required for an analysis)
"""

OVERFIT="""
The OFCCP requires a statistical analysis using regression models to evaluate impact of gender and other discriminatory factors
on pay. In order to run these analyses, there needs to be a balance between the number of employees being analyzed, and the 
number of variables used in the analysis.

In this case, there is an imbalance in the ratio of employees to number of features used. Please see the documentation for more information.
"""

PERFORMANCE="""
Each model we build is evaluated on how well it is able to predict someone's pay. If a model has a poor performance (i.e., struggle
to predict pay), the information that come out of the model (pay gaps, drivers of pay, etc.) might not be reliable.

In order to increase model performance, ensure that the pay philosophy is properly captured with the variables included. Poor performance
often suggest that there is a variable that can help predict pay, that is missing.
"""

BAD_GAPS="""
In regression exercises, there is a very common phenomenon called multicollinearity. This happens when two different variables are highly correlated/related to each other.
When this happens, the regression model struggles to properly identify the true impact of those collinear variables.

In this case, one of the illegitimate factors is highly correlated with another variable in the model and hence the pay gap report
for this variable cannot be trusted. Please see the documentation on how to address this probelm.
"""

BAD_COEF="""
In regression exercises, there is a very common phenomenon called multicollinearity. This happens when two different variables are highly correlated/related to each other.
When this happens, the regression model struggles to properly identify the true impact of those collinear variables.

In this case, one of the legitimate factors is highly correlated with another variable in the model and hence the pay gap report
for this variable cannot be trusted. Please see the documentation on how to address this probelm.
"""

VAL_PLACEHOLDER="""
No job groups have been identified. Please ensure that all the prior sections have been ran and that the "Run Analysis" button 
has been clicked and executed properly.

"""