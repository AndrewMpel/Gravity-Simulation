# Gravity Simulation: Celestial Mechanics & Accretion Simulator

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pygame](https://img.shields.io/badge/Library-Pygame-green.svg)
![Status](https://img.shields.io/badge/Status-Active--Development-brightgreen.svg)

A high-precision N-body gravitational interaction simulator developed in a Linux (Fedora) environment. This project simulates the orbital mechanics of our solar system—from Mercury to the dwarf planet Eris—using real-world mass and distance data.

## Engineering Highlights

* **N-Body Physics Engine:** Full implementation of Newton's Law of Universal Gravitation. Every celestial body dynamically exerts gravitational force on all others in every frame using the formula:
    $$F = G \frac{m_1 m_2}{r^2}$$
* **Accretion & Impact System:** An advanced collision system where bodies merge upon impact. It incorporates the **Conservation of Momentum** to calculate the resultant velocity of the newly formed mass:
    $$\vec{v}_{final} = \frac{m_1 \vec{v}_1 + m_2 \vec{v}_2}{m_1 + m_2}$$
* **World-Space Calculations:** All collision and physics logic is processed in real-world units (meters) rather than pixels, ensuring scientific accuracy regardless of the camera's zoom level.
* **Generative Orbital Paths:** Real-time path visualization using `collections.deque` for optimized memory management and performance ($O(1)$ append/pop operations).
* **Dynamic HUD & Labels:** Adaptive labels and circular hitboxes that scale and toggle based on the observer's focal length (Zoom level).

## Technical Specifications

* **Scale Factor:** `1 / 600,000,000` (Mapping astronomical distances to a visual interface).
* **Time Step (dt):** 20,000 simulated seconds per calculation step.
* **Kinematics:** Leverages `Vector2` math for all state vectors (Position, Velocity, Acceleration).

## Controls

| Action | Input |
| :--- | :--- |
| **Zoom In/Out** | Mouse Wheel |
| **Pan Camera** | Left Click & Drag |
| **Reset to Sun** | `Z` Key |
| **Planet Labels** | Automatically adaptive based on Zoom |

## Installation & Usage

1.  **Prerequisites:** Ensure you have Python 3 and Pygame installed:
    ```bash
    pip install pygame
    ```
2.  **Run the Simulation:**
    ```bash
    python app.py
    ```

---
**Andreas M.** *Informatics and Telecommunications Student*
