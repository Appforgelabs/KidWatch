#!/usr/bin/env python3
"""
KidWatch Autism Safety Scorer
Analyzes YouTube watch history and flags content based on patterns
known to be beneficial or concerning for children with autism.

Scoring is based on:
- Sensory profile (pacing, visual/audio intensity)
- Emotional regulation support
- Predictability and structure
- Educational and social value
- Channel quality consistency

This is a supplemental tool for parental awareness — not a medical assessment.
"""

# ─── CHANNELS KNOWN TO BE BENEFICIAL ───────────────────────────────────────
# Structured, predictable, emotion-coaching, autism-aware
GOOD_CHANNELS = {
    "Daniel Tiger's Neighborhood": {
        "reason": "Explicitly teaches emotional regulation, predictable structure, calming pace. PBS Kids — used in autism therapy programs.",
        "score": 5
    },
    "PBS KIDS": {
        "reason": "Curated educational content, structured, low stimulation, autism-inclusive (Sesame Street's Julia character).",
        "score": 5
    },
    "Sesame Street": {
        "reason": "Long-form educational, includes Julia (autistic character), emotional vocabulary building.",
        "score": 5
    },
    "Peppa Pig - Official Channel": {
        "reason": "Consistent characters, predictable episodes, gentle pacing. Official channel — highest quality control.",
        "score": 4
    },
    "Learn With Peppa Pig - Official Channel": {
        "reason": "Educational Peppa content — alphabet, feelings, structured learning. Good sensory profile.",
        "score": 5
    },
    "BabyBus - Kids Songs and Cartoons": {
        "reason": "Structured nursery content, consistent characters, teaches social rules and safety.",
        "score": 4
    },
    "Hoots & Tales": {
        "reason": "Calm animated read-alouds — predictable format, no sudden sounds, builds language and literacy.",
        "score": 5
    },
    "Bright Star Storytime": {
        "reason": "Gentle storytime format, consistent pacing, Leslie Patricelli books excellent for toddler emotional development.",
        "score": 5
    },
    "Little Wonders TV": {
        "reason": "Calm, structured educational gameplay. Daniel Tiger and Peppa Pig focused.",
        "score": 4
    },
    "Numberblocks": {
        "reason": "Highly structured, consistent visual grammar, great for pattern-loving kids. Low sensory overwhelm.",
        "score": 5
    },
    "Cocomelon - Nursery Rhymes": {
        "reason": "Predictable song structure, familiar characters, repetition is comforting.",
        "score": 4
    },
    "Super Simple Songs - Kids Songs": {
        "reason": "Slow, clear, repetitive songs — excellent for language development, low sensory load.",
        "score": 5
    },
}

# ─── CHANNELS TO REVIEW / FLAG ──────────────────────────────────────────────
# Not inherently harmful but worth parental awareness
REVIEW_CHANNELS = {
    "iGameplay1337": {
        "reason": "Rapid-cut app gameplay compilations. High visual pace, frequent transitions, minimal narration. Can be overstimulating.",
        "score": 2,
        "concern": "HIGH_PACE"
    },
    "AndromalicPlay1337": {
        "reason": "Similar to iGameplay1337 — fast-paced app reviews, minimal dialogue. Watch time without educational payoff.",
        "score": 2,
        "concern": "HIGH_PACE"
    },
    "Bulochka-TV": {
        "reason": "Mixed app gameplay compilations — unpredictable content mixing, rapid switches between games.",
        "score": 2,
        "concern": "HIGH_PACE"
    },
    "Quiz Noke": {
        "reason": "Logo sound quizzes — rapid audio bursts, unexpected sounds, no narrative structure. Potentially overstimulating for sensory-sensitive kids.",
        "score": 1,
        "concern": "SENSORY_OVERLOAD"
    },
    "Shery Quiz": {
        "reason": "Same concern as Quiz Noke — sudden loud sounds, rapid pacing, no educational structure.",
        "score": 1,
        "concern": "SENSORY_OVERLOAD"
    },
    "Quiz Tone": {
        "reason": "Logo sound quizzes — unexpected audio triggers, no predictable structure. High sensory stimulation.",
        "score": 1,
        "concern": "SENSORY_OVERLOAD"
    },
    "Great Quiz": {
        "reason": "Character comparison quizzes — unpredictable format, rapid image switching.",
        "score": 2,
        "concern": "HIGH_PACE"
    },
    "Blaze Kingdom": {
        "reason": "Character 'what they like' quizzes — low educational value, rapid visual content.",
        "score": 2,
        "concern": "LOW_VALUE"
    },
    "ROBIXX GAMING": {
        "reason": "Gaming walkthrough channel — no narration, minimal language learning value.",
        "score": 2,
        "concern": "LOW_VALUE"
    },
    "Gameplay Only": {
        "reason": "Silent gameplay — no verbal engagement, passive watching without narrative.",
        "score": 2,
        "concern": "LOW_VALUE"
    },
}

# ─── VIDEO TITLE KEYWORD FLAGS ──────────────────────────────────────────────
CONCERN_KEYWORDS = {
    "SENSORY_OVERLOAD": [
        "guess the sound", "logo sound", "sound quiz", "intro compilation",
        "sound challenge", "can you guess", "99% fail", "harder than you think",
        "mega compilation", "super compilation", "best compilation"
    ],
    "VIOLENT_OR_SCARY": [
        "scary", "horror", "jump scare", "death", "kill", "fight", "battle",
        "war", "monster", "demon", "evil", "terrifying", "nightmare"
    ],
    "INAPPROPRIATE": [
        "18+", "adults only", "mature", "inappropriate", "not for kids"
    ],
    "RAPID_PACING": [
        "38 games", "16 games", "all games", "every game", "compilation",
        "mega", "ultimate", "all episodes back to back"
    ]
}

POSITIVE_KEYWORDS = [
    "learn", "educational", "feelings", "emotions", "potty", "healthy habits",
    "read aloud", "storytime", "abc", "alphabet", "counting", "shapes", "colors",
    "safety", "kindness", "sharing", "friendship", "calm", "bedtime"
]


def score_video(video: dict) -> dict:
    """Score a single video and return enriched dict with flags."""
    title = video.get("title", "").lower()
    channel = video.get("channel", "")

    flags = []
    score = 3  # neutral default
    positive_signals = []

    # Channel-level scoring
    for ch_name, ch_data in GOOD_CHANNELS.items():
        if ch_name.lower() in channel.lower():
            score = max(score, ch_data["score"])
            positive_signals.append(ch_data["reason"])
            break

    for ch_name, ch_data in REVIEW_CHANNELS.items():
        if ch_name.lower() in channel.lower():
            score = min(score, ch_data["score"])
            flags.append({
                "type": ch_data["concern"],
                "message": f"Channel concern: {ch_data['reason']}"
            })
            break

    # Title-level keyword scanning
    for concern_type, keywords in CONCERN_KEYWORDS.items():
        if any(kw in title for kw in keywords):
            flags.append({
                "type": concern_type,
                "message": f"Title contains {concern_type.lower().replace('_', ' ')} pattern"
            })
            score = min(score, 2)

    for kw in POSITIVE_KEYWORDS:
        if kw in title:
            positive_signals.append(f"Contains '{kw}' — positive developmental signal")
            score = min(5, score + 0)  # don't inflate, just note it

    # Final rating
    if score >= 4:
        rating = "good"
        badge = "✅"
    elif score == 3:
        rating = "neutral"
        badge = "⬜"
    elif score == 2:
        rating = "review"
        badge = "⚠️"
    else:
        rating = "flag"
        badge = "🚩"

    return {
        **video,
        "safety_score": score,
        "safety_rating": rating,
        "safety_badge": badge,
        "flags": flags,
        "positive_signals": positive_signals[:2],
    }


def analyze_history(history: dict) -> dict:
    """Run full safety analysis on watch history."""
    videos = history.get("videos", [])
    scored = [score_video(v) for v in videos]

    flagged = [v for v in scored if v["safety_rating"] in ("flag", "review")]
    good = [v for v in scored if v["safety_rating"] == "good"]
    neutral = [v for v in scored if v["safety_rating"] == "neutral"]

    # Channel-level summary
    from collections import Counter, defaultdict
    channel_scores = defaultdict(list)
    for v in scored:
        channel_scores[v["channel"]].append(v["safety_score"])

    channel_summary = []
    for ch, scores in sorted(channel_scores.items(), key=lambda x: len(x[1]), reverse=True):
        avg = sum(scores) / len(scores)
        if avg <= 2:
            badge = "🚩"
        elif avg <= 2.9:
            badge = "⚠️"
        elif avg >= 4:
            badge = "✅"
        else:
            badge = "⬜"
        channel_summary.append({
            "channel": ch,
            "video_count": len(scores),
            "avg_score": round(avg, 1),
            "badge": badge
        })

    # Concern type breakdown
    all_flags = []
    for v in flagged:
        for f in v.get("flags", []):
            all_flags.append(f["type"])
    concern_counts = dict(Counter(all_flags).most_common())

    return {
        **history,
        "safety": {
            "generated": __import__("datetime").datetime.now().isoformat(),
            "total_scored": len(scored),
            "good_count": len(good),
            "neutral_count": len(neutral),
            "review_count": len([v for v in scored if v["safety_rating"] == "review"]),
            "flag_count": len([v for v in scored if v["safety_rating"] == "flag"]),
            "concern_breakdown": concern_counts,
            "channel_summary": channel_summary[:20],
            "flagged_videos": [
                {"title": v["title"], "channel": v["channel"],
                 "badge": v["safety_badge"], "flags": v["flags"]}
                for v in flagged[:30]
            ],
        },
        "videos": scored
    }


if __name__ == "__main__":
    import json
    from pathlib import Path

    DATA = Path(__file__).parent.parent / "data" / "history.json"
    history = json.loads(DATA.read_text())
    result = analyze_history(history)
    DATA.write_text(json.dumps(result, indent=2))

    s = result["safety"]
    print(f"\n📊 Safety Analysis Complete")
    print(f"  ✅ Good:    {s['good_count']} videos")
    print(f"  ⬜ Neutral: {s['neutral_count']} videos")
    print(f"  ⚠️  Review:  {s['review_count']} videos")
    print(f"  🚩 Flag:    {s['flag_count']} videos")
    print(f"\n🚩 Top concerns: {s['concern_breakdown']}")
    print(f"\nChannel breakdown (top flagged):")
    for ch in s["channel_summary"]:
        if ch["badge"] in ("🚩", "⚠️"):
            print(f"  {ch['badge']} {ch['channel']} ({ch['video_count']} videos, avg score {ch['avg_score']})")
