# telma
Welcomo to Telma's Library.

![image](https://user-images.githubusercontent.com/67124439/126873444-3ee1e47d-f833-42da-bb75-6c4818c94c66.png)

This library is composed by 5 Classes. Namely:

* BiometricModel.
* OneLife
* MultipleLives
* SpainOperation
* InsuranceBenefits

Plotting functions are located in **OneLife** or **MultiplesLives** classes.

Besides the "classic static" manner of plotting in life actuarial science. **<font color='navy'>Telma</font>** permits plotting charts **interactively.**

---
## Plotting using OneLife and MultipleLives (statically).
---

##### OneLife
It will be possible to graph either from a cohort function or several. <br>
* For plotting **one cohort**,  **OneLife** will be used.<br>
* For plotting **more than one cohorts**, **MultipleLives.** will be used. <br>

Example with one cohort: **Usa_Male**.


Invoking OneLife, *lifeplot* method has as parameters:
* **cohort1**. It refers to the cohort to be passed.
* **interactive**. If true an interactive chart will be plotted using *Plotly*.
* **death**. It refers to the numbers of death chart $d(x)$, if True when plotting interactively it will show the number of death chart.
* **qx_log**. It refers to the probability of death in logarithmic scale, that is $log(q(x))$. If True when plotting interactively it will show $log(q(x))$.




##### MultipleLives

### The question: do I want to plot more cohorts?
##### Follow the same steps as OneLife ().lifeplot but with:

* MultipleLives $\rightarrow$ **lifeplot_2** method
* **Two cohorts**. That is, by default at least two parameters will be needed; $ l_x $ and $l_y$ the cohort functions 
* A third cohort can be passed, if perhaps you want to confront a model.

<br> Example: usa_male, usa_female and a "model".


![image](https://user-images.githubusercontent.com/67124439/126873575-399c4389-3696-48fc-9986-c15a3d094b61.png)

For view some example of interactive plot, click the following link. [1 Plotting Telma](https://nbviewer.jupyter.org/github/Joevalencia/telma/blob/main/1%20Plotting-example.ipynb)
