# 🤖 Robot – Embedded Control System

This repository contains the full software stack used to control an autonomous robot.  
The code is designed with a modular architecture to ensure scalability, readability, and ease of integration.

---

## ⚙️ Features

- 🚗 Robot motion control (forward, turning, maneuvers)
- 🎯 Encoder-based position tracking
- 🧭 IMU integration (gyro / accelerometer)
- 📡 WiFi communication and remote control
- 🧠 Embedded decision-making logic
- 🤖 Task execution (object placement / deposit)

---

## 🧠 Project Architecture
📁 root
├── main.py # Main entry point
├── boot.py # System initialization
├── lib/ # Core modules
│ ├── mouv.py # Movement control
│ ├── enco.py # Encoder handling
│ ├── gyro.py # Gyroscope
│ ├── mpu9250.py # IMU driver
│ ├── wifi.py # WiFi communication
│ ├── avancer_wifi.py # Remote movement
│ ├── intelligent.py # Decision logic
│ ├── depo.py # Object deposit
│ ├── placer_jouet.py # Object placement
│ ├── depot_jouet.py # Task routines
│ ├── temps.py # Time management
│ └── blink.py # LED feedback


---

## 🧩 Technologies

- **MicroPython / Embedded Python**
- **IMU sensors** (MPU9250 / MPU6500)
- **Quadrature encoders**
- **Wireless communication (WiFi)**

---

## 🎯 Objectives

The goal of this project is to develop a reliable autonomous robot capable of:
- Navigating its environment with precision
- Making decisions based on sensor data
- Executing predefined tasks autonomously

---

## 🚀 Getting Started

1. Flash MicroPython on your microcontroller
2. Upload the project files
3. Run:

```bash
main.py
