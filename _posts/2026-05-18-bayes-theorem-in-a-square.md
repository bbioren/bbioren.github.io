---
layout: post
title: bayes' theorem in a square
date: 2026-05-18
description: conditioning is zooming in, and the base rate decides what you see when you get there
tags: visual-proofs probability bayes
categories: math
related_posts: false
---

Bayes' theorem is usually presented as a formula to memorize, which is odd, because it is one line of algebra away from the definition of conditional probability. And yet the classic question it answers, "you tested positive for a rare disease, how worried should you be?", is one that people get badly wrong, trained professionals included. Studies have repeatedly put this question to doctors, and many of the answers come back far too high. The algebra isn't the hard part. The intuition is. So let's draw it.

## The statement

For events $$H$$ (a hypothesis, say "sick") and $$E$$ (evidence, say "tested positive") with $$P(E) \gt 0$$,

$$
P(H \mid E) = \frac{P(E \mid H)\, P(H)}{P(E)}, \qquad P(E) = P(E \mid H)\,P(H) + P(E \mid \neg H)\,P(\neg H).
$$

The proof is just writing $$P(H \cap E)$$ two ways: it equals $$P(H \mid E)\,P(E)$$ and also $$P(E \mid H)\,P(H)$$. Set them equal and divide.

Here's the heuristic I find most useful. Conditioning on $$E$$ means _zooming in_: throw away every outcome where $$E$$ didn't happen, then rescale what's left so it has total probability 1 again. So $$P(H \mid E)$$ is "what fraction of the $$E$$-world is also $$H$$." The numerator $$P(E \mid H)P(H)$$ is the size of the overlap, and the denominator $$P(E)$$ is the size of the world you zoomed into. Two sanity checks: if $$E$$ is certain, nothing gets thrown away and $$P(H \mid E) = P(H)$$. If $$E$$ can only happen under $$H$$ (so $$P(E \mid \neg H) = 0$$), the denominator collapses onto the numerator and $$P(H \mid E) = 1$$.

## The medical test

Suppose a disease has prevalence $$P(H) = 0.01$$. The test has sensitivity $$P(E \mid H) = 0.90$$ and a false positive rate of $$P(E \mid \neg H) = 0.09$$. You test positive. Then

$$
P(H \mid E) = \frac{0.90 \times 0.01}{0.90 \times 0.01 + 0.09 \times 0.99} = \frac{0.009}{0.009 + 0.0891} = \frac{0.009}{0.0981} \approx 0.0917.
$$

About 9.2%. A test that catches 90% of sick people and clears 91% of healthy ones leaves a positive patient less than one-in-ten likely to be sick.

There's a cleaner way to run this computation. Divide Bayes' theorem for $$H$$ by Bayes' theorem for $$\neg H$$. The $$P(E)$$ cancels, and what's left is

$$
\underbrace{\frac{P(H \mid E)}{P(\neg H \mid E)}}_{\text{posterior odds}} = \underbrace{\frac{P(E \mid H)}{P(E \mid \neg H)}}_{\text{likelihood ratio}} \times \underbrace{\frac{P(H)}{P(\neg H)}}_{\text{prior odds}}.
$$

For our test the likelihood ratio is $$0.90 / 0.09 = 10$$ and the prior odds are $$1 : 99$$, so the posterior odds are $$10 : 99$$, and $$P(H \mid E) = 10/109 \approx 0.0917$$. Same answer, no denominators to expand. This is the version worth remembering: a test is summarized by a single number, its likelihood ratio, and a positive result multiplies your odds by it.

## The proof, in a square

Take the unit square as the space of all outcomes, with area as probability. Cut it with one vertical line at $$x = P(H)$$: the thin strip on the left is the sick people, the wide strip on the right is the healthy people. Inside each strip, shade the bottom part where the test comes back positive. In the sick strip the shaded height is $$P(E \mid H)$$, and in the healthy strip it's $$P(E \mid \neg H)$$. Each shaded piece is a rectangle, so its area is width times height, which is exactly $$P(H \cap E) = P(H)\,P(E \mid H)$$ on the left and $$P(\neg H \cap E) = P(\neg H)\,P(E \mid \neg H)$$ on the right.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/bayes-theorem-in-a-square/unit-square-to-scale.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The unit square drawn to scale for prevalence 1%, sensitivity 90%, false positive rate 9%. The sick strip really is that thin; the shaded (positive-test) region is the orange sliver plus the dark blue band.
</div>

I've drawn this to scale on purpose. The sick strip is so thin you can barely see it, and that is the whole point. The event "tested positive" is the union of the two shaded rectangles. The orange one is tall but skinny, and the blue one is short but wide, and when you compare areas instead of heights, the blue one wins by almost a factor of ten: $$0.0891$$ versus $$0.009$$.

Now condition on $$E$$. Throw away everything unshaded, and rescale the remaining area to 1.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/bayes-theorem-in-a-square/zoom-to-positives.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  After zooming in to the positive region and renormalizing, the sick share is 0.009 out of 0.0981, about 9.2%.
</div>

The fraction of the new world that is orange is

$$
P(H \mid E) = \frac{\text{area of orange rectangle}}{\text{total shaded area}} = \frac{P(H)\,P(E \mid H)}{P(H)\,P(E \mid H) + P(\neg H)\,P(E \mid \neg H)},
$$

which is Bayes' theorem, read straight off the picture. The odds form is in there too: the ratio of the two shaded areas is (ratio of widths) times (ratio of heights), which is prior odds times likelihood ratio.

## The part that gets missed

The square makes the most common mistake visible: $$P(E \mid H)$$ is a _height_ inside one strip, while $$P(H \mid E)$$ is a _share of area_ across both strips. They are different numbers, and treating them as the same is the confusion of the inverse. In a courtroom it's called the prosecutor's fallacy, as in "an innocent person would match this evidence only 1% of the time, so there's a 99% chance the defendant is guilty." The heights tell you how good the test is. They don't tell you how wide the strips are, and when the hypothesis is rare, the strip width dominates. A 9% false positive rate applied to 99% of the population simply produces more positives than a 90% hit rate applied to 1%. The prior isn't a technicality you can wave away. When $$H$$ is rare, it's most of the answer.

That also tells you what to do next. Run a second, independent test and it comes back positive too. The odds get multiplied by the likelihood ratio again, going from $$10 : 99$$ to $$100 : 99$$, so $$P(H \mid E_1, E_2) = 100/199 \approx 50\%$$. In the picture, you zoom into the shaded region and shade it again. But that multiplication assumes the two results are _conditionally independent given the disease status_. If the false positives come from something about the patient that a retest will pick up again, a repeat positive carries much less information than the formula claims. The likelihood ratio does all the work in Bayes' theorem, and you only get to apply it twice when the second piece of evidence really is new.
