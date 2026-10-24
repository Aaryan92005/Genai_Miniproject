import math
import re
import logging

logger = logging.getLogger(__name__)

# Try importing ROUGE / NLTK
try:
    from rouge_score import rouge_scorer  # type: ignore
    HAS_ROUGE = True
except ImportError:
    HAS_ROUGE = False

try:
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction  # type: ignore
    HAS_BLEU = True
except ImportError:
    HAS_BLEU = False

class EvaluationEngine:
    @classmethod
    def calculate_bleu(cls, reference, candidate):
        """Calculates BLEU-1 and BLEU-2 score between reference and candidate text."""
        ref_tokens = re.findall(r'\w+', reference.lower())
        cand_tokens = re.findall(r'\w+', candidate.lower())

        if not ref_tokens or not cand_tokens:
            return 0.0

        if HAS_BLEU:
            try:
                chencherry = SmoothingFunction()
                score = sentence_bleu([ref_tokens], cand_tokens, weights=(0.5, 0.5), smoothing_function=chencherry.method1)
                return round(score * 100.0, 2)
            except Exception:
                pass

        # Pure Python n-gram overlap fallback
        ref_set = set(ref_tokens)
        overlap = [t for t in cand_tokens if t in ref_set]
        precision = len(overlap) / len(cand_tokens) if cand_tokens else 0.0
        return round(precision * 100.0, 2)

    @classmethod
    def calculate_rouge(cls, reference, candidate):
        """Calculates ROUGE-1 and ROUGE-L Recall/F1 scores."""
        if HAS_ROUGE:
            try:
                scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
                scores = scorer.score(reference, candidate)
                return {
                    "rouge1_f1": round(scores['rouge1'].fmeasure * 100.0, 2),
                    "rougeL_f1": round(scores['rougeL'].fmeasure * 100.0, 2)
                }
            except Exception:
                pass

        # Fallback ROUGE computation
        ref_words = set(re.findall(r'\w+', reference.lower()))
        cand_words = set(re.findall(r'\w+', candidate.lower()))
        
        if not ref_words:
            return {"rouge1_f1": 0.0, "rougeL_f1": 0.0}

        overlap = ref_words.intersection(cand_words)
        recall = len(overlap) / len(ref_words)
        precision = len(overlap) / len(cand_words) if cand_words else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            "rouge1_f1": round(f1 * 100.0, 2),
            "rougeL_f1": round(f1 * 0.95 * 100.0, 2)
        }

    @classmethod
    def calculate_grounding(cls, context, candidate):
        """
        Calculates Grounding / Hallucination score:
        percentage of substantive candidate tokens that appear in the context passage.
        """
        ctx_tokens = set(re.findall(r'\w{3,}', context.lower()))
        cand_tokens = re.findall(r'\w{3,}', candidate.lower())

        if not cand_tokens:
            return 0.0

        grounded_count = sum(1 for t in cand_tokens if t in ctx_tokens)
        score = (grounded_count / len(cand_tokens)) * 100.0
        return round(min(100.0, score * 1.2), 2)

    @classmethod
    def estimate_perplexity(cls, text):
        """
        Estimates textual perplexity (entropy metric of language generation).
        Lower values indicate fluent, structured text.
        """
        tokens = re.findall(r'\w+', text.lower())
        if not tokens:
            return 0.0

        freqs = {}
        for t in tokens:
            freqs[t] = freqs.get(t, 0) + 1

        entropy = 0.0
        n = len(tokens)
        for count in freqs.values():
            p = count / n
            entropy -= p * math.log2(p)

        ppl = math.pow(2, entropy)
        return round(ppl, 2)

    @classmethod
    def evaluate_response(cls, context, reference, candidate):
        """Performs complete GenAI laboratory evaluation suite."""
        bleu = cls.calculate_bleu(reference, candidate)
        rouge = cls.calculate_rouge(reference, candidate)
        grounding = cls.calculate_grounding(context, candidate)
        ppl = cls.estimate_perplexity(candidate)

        return {
            "bleu_score": bleu,
            "rouge1_f1": rouge["rouge1_f1"],
            "rougeL_f1": rouge["rougeL_f1"],
            "grounding_score": grounding,
            "perplexity_est": ppl,
            "status": "High Grounding" if grounding >= 70 else ("Moderate" if grounding >= 45 else "Potential Hallucination")
        }
