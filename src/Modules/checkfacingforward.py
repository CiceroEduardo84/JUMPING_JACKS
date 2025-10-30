def checkfacingforward(landmarks, pose):
    nariz = landmarks.landmark[pose.PoseLandmark.NOSE]

    visibilidade = nariz.visibility if hasattr(nariz, 'visibility') else 1.0
    
    return (visibilidade > 0.5) and (0.3 < nariz.x < 0.7)
