const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export const submitFalsePositiveFeedback = async (text, correctedEntities) => {
  try {
    const response = await fetch(`${API_URL}/feedback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: text,
        is_false_positive: true,
        corrected_entities: correctedEntities
      })
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("Failed to submit feedback for LoRA retraining", error);
    return null;
  }
};
