# TES-LCA Demo README

An absolute environmental sustainability assessment framework based on ecosystem services 

## 💻 How to Use
* Downlocal shreapsheet template
* Fill in process information, technology matrix, inventory matrix and weighting vector
* Upload files
* Variable selection
    * Sharing principle name
    * Framework used
    * Geospatial scales 
*  Click 'Run' 🖱️ 
* 🎉🎉You just got the absolute environmental sustainability result for your system🎉🎉


## 👀 Examples
### Unit process - Corn Farm 🌽

![farm](https://github.com/YingX110/TESdemo/raw/interface/images/cornfarm.png)

### Geo-unit process - States in Great Lakes Region 🌎
* **Ecosystem service**: carbon sequestration service
* **Biophysical model/tool**: iTree-Canopy
* **Geospatial scale of ES**: local (state), country, global 
* **Compare different sharing principles**:
    * Demand
    * Population
    * GDP
    * Inverse of GDP
    * Area



### LCA - Soybean Biodiesel Production ⛽
![BD](https://github.com/YingX110/TESdemo/raw/interface/images/BD.png)


## ✏️ Exercises
### 1. For the corn farm exanple, try different locations and compare the result
### 2. Quantify the Absolute Environmental Sustainability for PET-Bottle Production 🍼
* Functional unit: 2000 million bottles
* Technology matrix: $$A = \begin{bmatrix} 1 & 0 & 0 & -4\\0 & 1 & 0 & -60 \\0 & 0 & 1 & -1 \\0 & 0 & 0 & 1 \end{bmatrix}$$
* Inventory matrix: $$D = \begin{bmatrix} 2.62e-6 & 0 & 0 & 0\\0 & 2.26e-6 & 0 & 0 \\0 & 0 & 2.22e-6 \\0 & 0 & 0 & 1e-5 \end{bmatrix}$$
* Weighting vector: $ wt = [1, 1, 1, 1] $
* Flow diagram and system boundary is shown as belows

![bottle](https://github.com/YingX110/TESdemo/raw/interface/images/petbottle.svg)
