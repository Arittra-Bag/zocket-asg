from rouge_score import rouge_scorer
from collections import Counter
import math
import re

# Input Texts
original = "Get 50% off on all our summer shoes collection!"
rewrites = {
    "Meta": "Ready for some summer shoe magic? ☀️ Our entire collection is now 50% off! Step into style without breaking the bank. Shop now and elevate your seasonal look! #SummerShoes #ShoeSale #50PercentOff #SummerStyle",
    "Google": "Summer Shoes Sale – 50% Off Now\nElevate your summer footwear collection. Enjoy significant savings on all styles for a limited period.",
    "LinkedIn": "As summer approaches, we invite you to explore our latest footwear collection with a special offer. We're pleased to provide 50% off all summer shoes..."
}

# Simple BLEU-1 implementation
def simple_bleu1(reference, hypothesis):
    ref_words = reference.lower().split()
    hyp_words = hypothesis.lower().split()
    
    if len(hyp_words) == 0:
        return 0.0
    
    ref_counter = Counter(ref_words)
    hyp_counter = Counter(hyp_words)
    
    # Count matching unigrams
    matches = 0
    for word in hyp_counter:
        matches += min(hyp_counter[word], ref_counter.get(word, 0))
    
    precision = matches / len(hyp_words)
    
    # Apply brevity penalty
    brevity_penalty = 1.0
    if len(hyp_words) < len(ref_words):
        brevity_penalty = math.exp(1 - len(ref_words) / len(hyp_words))
    
    return brevity_penalty * precision

# Calculate relevance based on keyword overlap
def calculate_relevance(original, rewrite):
    # Extract key concepts from original
    original_lower = original.lower()
    rewrite_lower = rewrite.lower()
    
    # Define key concepts to check
    key_concepts = {
        'discount': ['50%', 'off', 'sale', 'savings', 'discount'],
        'product': ['shoes', 'footwear', 'collection'],
        'season': ['summer']
    }
    
    concept_scores = []
    for concept, keywords in key_concepts.items():
        original_has = any(kw in original_lower for kw in keywords)
        rewrite_has = any(kw in rewrite_lower for kw in keywords)
        if original_has and rewrite_has:
            concept_scores.append(1.0)
        elif original_has and not rewrite_has:
            concept_scores.append(0.0)
        else:
            concept_scores.append(0.5)
    
    return sum(concept_scores) / len(concept_scores) if concept_scores else 0.0

# Detect hallucination (new information not in original)
def detect_hallucination(original, rewrite):
    original_lower = original.lower()
    rewrite_lower = rewrite.lower()
    
    # Extract numbers from both texts
    original_numbers = set(re.findall(r'\d+', original))
    rewrite_numbers = set(re.findall(r'\d+', rewrite))
    
    # Check for new numbers (potential hallucination)
    new_numbers = rewrite_numbers - original_numbers
    hallucination_score = 0.0
    
    if new_numbers:
        hallucination_score += 0.3
    
    # Check for specific claims not in original
    hallucination_phrases = [
        'limited time', 'limited period', 'while supplies last',
        'free shipping', 'best seller', 'customer favorite',
        'award winning', 'exclusive', 'new arrival'
    ]
    
    for phrase in hallucination_phrases:
        if phrase in rewrite_lower and phrase not in original_lower:
            hallucination_score += 0.1
    
    # Cap at 1.0
    return min(hallucination_score, 1.0)

# Calculate F1 score based on word overlap
def calculate_f1(original, rewrite):
    original_words = set(original.lower().split())
    rewrite_words = set(rewrite.lower().split())
    
    # Remove common stop words for better accuracy
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
    original_words = original_words - stop_words
    rewrite_words = rewrite_words - stop_words
    
    if not rewrite_words:
        return 0.0
    
    # Calculate precision and recall
    overlap = original_words & rewrite_words
    precision = len(overlap) / len(rewrite_words) if rewrite_words else 0
    recall = len(overlap) / len(original_words) if original_words else 0
    
    # Calculate F1
    if precision + recall == 0:
        return 0.0
    
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1

# Scoring setup
scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

print("Evaluation Results for Ad Rewrites")
print("=" * 60)

for platform, text in rewrites.items():
    rouge = scorer.score(original, text)['rougeL'].fmeasure
    bleu = simple_bleu1(original, text)
    relevance = calculate_relevance(original, text)
    hallucination = detect_hallucination(original, text)
    f1 = calculate_f1(original, text)
    
    print(f"\nPlatform: {platform}")
    print(f"ROUGE-L:       {rouge:.4f}")
    print(f"BLEU-1:        {bleu:.4f}")
    print(f"F1 Score:      {f1:.4f}")
    print(f"Relevance:     {relevance:.4f} (1.0 = highly relevant)")
    print(f"Hallucination: {hallucination:.4f} (0.0 = no hallucination)")

print("\n" + "=" * 60)
print("Metric Explanations:")
print("- ROUGE-L: Measures longest common subsequence overlap")
print("- BLEU-1: Measures unigram precision with brevity penalty")
print("- F1 Score: Harmonic mean of precision and recall for word overlap")
print("- Relevance: Checks if key concepts from original are preserved")
print("- Hallucination: Detects new information not present in original")
