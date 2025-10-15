# 🌀 Aeroacoustic Optimization of UAV Propellers  
### Bio-Inspired and Geometric Design Modifications for Noise Reduction

---

## 📘 Overview
This project investigates **bio-inspired and advanced geometric UAV propeller designs** to achieve a **minimum 15% reduction in noise-to-thrust ratio (TNR)** compared to standard commercial propellers.  
Our study combines **experimental testing**, **aeroacoustic signal processing**, and **CFD simulation** to identify how natural mechanisms—like **owl serrations** and **whale tubercles**—influence propeller noise behavior.

This repository includes all **Python analysis scripts, CAD models, CFD data,** and **experimental logs** for reproducibility and further research.

---

## 🎯 Objectives
- Design, fabricate, and test **bio-inspired propeller geometries**.  
- Analyze **acoustic signatures** using FFT and SPL calculations.  
- Compute **Thrust-to-Noise Ratio (TNR)** across propeller variants.  
- Use **CFD (Ansys Fluent / SimScale)** to visualize vortex formation and pressure fields.  
- Assess **psychoacoustic perception** of modified propeller sounds.  

---

## 🧩 Design Strategies
| Design Inspiration | Mechanism | Expected Effect |
|--------------------|------------|-----------------|
| 🦉 **Owl-Inspired Serrations** | Serrated trailing edges disrupt vortex shedding | Lower tonal noise |
| 🐋 **Whale-Inspired Tubercles** | Sinusoidal leading-edge bumps delay stall | Reduced tip vortex noise |
| ⛳ **Golf Ball Dimples** | Surface dimples control boundary layer separation | Lower broadband turbulence |
| 🌀 **Toroidal Blades** | Closed-loop blade eliminates tip vortices | Smoother noise spectrum |
| ✈️ **Winglets (Hoerner & Endplate)** | Minimize vortex shedding at tips | Reduced high-frequency peaks |
| 🚁 **Zipline Geometry** | Uneven spacing spreads tonal peaks | Improved psychoacoustic comfort |

---

## ⚙️ Experimental Setup
- **Thrust Measurement:** Calibrated thrust stand with Arduino data logging  
- **Acoustic Measurement:** Calibrated UMIK-1 condenser microphone (1 m off-axis)  
- **RPM Control:** Optical tachometer + ESC regulation via Arduino  
- **Environment:** Semi-anechoic box with foam acoustic dampening  
- **Power Supply:** Regulated 12 V DC PSU for motor consistency  

All tests are performed at a **constant 10,000 RPM** for direct comparison between propeller designs.

---

## 🧠 Data Processing & Analysis

### 🧾 Acoustic Equations
\[
SPL (dB) = 20 \log_{10} \left( \frac{p}{p_0} \right)
\]
\[
TNR = \frac{T}{10^{SPL/20}}
\]

### 📊 Python Workflow
- **Data Acquisition:** Microphone + Arduino (thrust, RPM, voltage)
- **FFT Analysis:** Frequency decomposition using `numpy.fft`
- **SPL Computation:** A-weighted loudness with `scipy.signal`
- **TNR Calculation:** Real-time ratio computation
- **Visualization:** Spectrograms, SPL histograms, and thrust vs noise plots

---

## 💻 Repository Structure - TBD
