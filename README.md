
# FaciaFix Mobile Application

FaciaFix is an AI-driven mobile application designed for the diagnosis and classification of facial paralysis, specifically Bell’s Palsy, using advanced deep learning and computer vision techniques. The app leverages facial landmark detection and quantitative analysis to assess facial asymmetry in real-time, offering an accessible, non-invasive solution for clinicians and patients.

## Overview
FaciaFix addresses the limitations of traditional diagnostic methods by providing a portable and cost-effective mobile application. The app uses deep learning models trained on the YouTube FP (YFP) dataset to classify facial paralysis severity. It analyzes three key facial movements: smiling, eye closure, and eyebrow elevation, offering objective assessments based on facial landmarks.

## Key Features
- Real-time diagnosis using MediaPipe's 478 facial landmarks for accurate 3D face mesh generation.
- Classification of severity into four categories: mild, moderate, moderately severe, and severe.
- Quantitative analysis of facial asymmetry based on distances between key facial landmarks.
- Cross-platform compatibility with an easy-to-use interface for both doctors and patients.

## Data and Models
- **Dataset**: The YouTube FP (YFP) dataset, containing videos of 21 Bell’s Palsy patients, was re-labeled using the House-Brackmann (HB) grading scale to ensure accuracy.

- **Preprocessing**:
  - Videos were converted into frames at 6 FPS and labeled based on three facial movements: smiling, eyebrow elevation, and eye closure.
  - Data augmentation (e.g., rotation, noise) was applied to enhance model generalization and robustness.

- **Deep Learning Models**:
  - **MobileNet (Transfer Learning)**: Best-performing model with an accuracy of 0.9812, precision of 0.9753, recall of 0.9727, and F1 score of 0.974.
  - **CNN**: Accuracy of 0.9565.
  - **MLP**: Accuracy of 0.923.
  - **VGG16**: Achieved 0.9278 accuracy with precision of 0.9523.
  - **Vision Transformer**: Accuracy of 0.7559, requiring further tuning.

## Quantitative Assessment
- **Eyebrows**: Assessed by measuring the distance between the nose tip and eyebrow arches to evaluate symmetry.
- **Mouth**: Symmetry analyzed using the distance between the nose tip and the corners of the mouth.
- **Eyes**: Eye closure is evaluated based on the area of the eyes, providing an accurate measure of paralysis.

## Technical Stack
- **Back-End**: Developed using Django REST Framework (DRF) for efficient API handling.
- **Front-End**: Built with React Native, enabling cross-platform development for iOS and Android.
- **Database**: SQLite is used for local data storage, with cloud integration through AWS for secure remote access.
- **Development Tools**: Android Studio is used for testing and deployment on Android devices, with Redux Toolkit for state management.

## Publication
This project has been published in the Journal of Physics: Conference Series. You can access the full paper here:
[FaciaFix: AI-Based Mobile Application for Diagnosis and Classification of Facial Paralysis](https://iopscience.iop.org/article/10.1088/2057-1976/ad8094)

## Contributions
| Team Members                                        | Role            |  
| -------------                                       | -------------   |
| [Doha Eid](https://github.com/doha-eid)             | Deep Learning   |
| [Maye Khaled](https://github.com/mayekhaled0)       | Deep Learning   |
| [Mariam Ezzat](https://github.com/mariamezzat01)    | Back-End        |
| [Amira Mohamed](https://github.com/AmeeraMOhammed)  | Front-End       |
| [Mayar Ehab](https://github.com/mayarehab)          | Front-End       |

## Explainer Video
Watch a brief explainer video about FaciaFix: [See Video](https://www.youtube.com/watch?v=7rBY8yRraek&list=PLa9SfMu7FWOStQO70kPCivXEDQDjjXdRc&index=5)
