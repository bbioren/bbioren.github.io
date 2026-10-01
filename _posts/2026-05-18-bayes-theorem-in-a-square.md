---
layout: post
title: bayes' theorem in a square
date: 2026-05-18
description: a positive test for a rare disease, drawn to scale
tags: visual-proofs probability bayes
categories: math
related_posts: false
---

Bayes' theorem usually gets taught as a formula to memorize, which is a little strange, since it's one line of algebra away from the definition of conditional probability. Take a hypothesis $$H$$ (say "sick") and some evidence $$E$$ (say "tested positive"). You can write $$P(H \cap E)$$ as $$P(H \mid E)\,P(E)$$ or as $$P(E \mid H)\,P(H)$$, and if you set those equal and divide by $$P(E)$$ you get

$$
P(H \mid E) = \frac{P(E \mid H)\, P(H)}{P(E)}, \qquad P(E) = P(E \mid H)\,P(H) + P(E \mid \neg H)\,P(\neg H).
$$

So the algebra is easy. The intuition is what's hard, and the standard question shows it. You test positive for a rare disease, so how worried should you be? People are bad at this one, and that includes doctors, who've been asked versions of it in studies and often answer way too high.

## The test

Say the disease has prevalence $$P(H) = 0.01$$, the test has sensitivity $$P(E \mid H) = 0.90$$, and its false positive rate is $$P(E \mid \neg H) = 0.09$$. You test positive. Plugging in,

$$
P(H \mid E) = \frac{0.90 \times 0.01}{0.90 \times 0.01 + 0.09 \times 0.99} = \frac{0.009}{0.009 + 0.0891} = \frac{0.009}{0.0981} \approx 0.0917.
$$

That's about 9.2%. A test that catches 90% of sick people and clears 91% of healthy people still leaves you with less than a one-in-ten chance of being sick after a positive result. If that seems wrong to you, you're in good company.

There's a nicer way to run this computation. Write Bayes' theorem for $$H$$ and for $$\neg H$$ and divide one by the other. The $$P(E)$$ cancels and you're left with

$$
\underbrace{\frac{P(H \mid E)}{P(\neg H \mid E)}}_{\text{posterior odds}} = \underbrace{\frac{P(E \mid H)}{P(E \mid \neg H)}}_{\text{likelihood ratio}} \times \underbrace{\frac{P(H)}{P(\neg H)}}_{\text{prior odds}}.
$$

For our test the likelihood ratio is $$0.90 / 0.09 = 10$$ and the prior odds are $$1 : 99$$, so the posterior odds are $$10 : 99$$ and $$P(H \mid E) = 10/109 \approx 0.0917$$. Same answer, and nothing to expand. I like this version a lot more. The whole test gets boiled down to one number, and a positive result multiplies your odds by that number. Starting from $$1 : 99$$, multiplying by 10 just doesn't get you very far.

## The square

OK, so let's draw it. Take the unit square as the set of all outcomes, with area as probability. Draw a vertical line at $$x = P(H)$$, so the thin strip on the left is the sick people and the wide strip on the right is the healthy people. Then in each strip shade the bottom part, where the test comes back positive. The shaded height is $$P(E \mid H)$$ on the left and $$P(E \mid \neg H)$$ on the right. Each shaded piece is a rectangle, so its area is width times height, which is exactly $$P(H \cap E) = P(H)\,P(E \mid H)$$ on the left and $$P(\neg H \cap E) = P(\neg H)\,P(E \mid \neg H)$$ on the right.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/bayes-theorem-in-a-square/unit-square-to-scale.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The square drawn to scale for prevalence 1%, sensitivity 90%, false positive rate 9%. The positive-test region is the orange sliver plus the dark blue band.
</div>

I drew it to scale on purpose, and you can see the sick strip is so thin it's barely there. The positive region is made of two rectangles, an orange one that's tall and skinny and a blue one that's short and wide. If you compare their areas instead of their heights, the blue one wins by almost a factor of ten ($$0.0891$$ versus $$0.009$$).

Conditioning on $$E$$ means zooming in. Throw away everything that isn't shaded, and rescale what's left so it has area 1 again.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/bayes-theorem-in-a-square/zoom-to-positives.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Zoomed in to the positive region. The sick share is 0.009 out of 0.0981, about 9.2%.
</div>

The fraction of this new world that's orange is

$$
P(H \mid E) = \frac{\text{area of orange rectangle}}{\text{total shaded area}} = \frac{P(H)\,P(E \mid H)}{P(H)\,P(E \mid H) + P(\neg H)\,P(E \mid \neg H)},
$$

and that's Bayes' theorem, read off the picture. The odds form is in there too, since the ratio of the two shaded areas is the ratio of the widths times the ratio of the heights, which is prior odds times likelihood ratio.

The picture also shows what goes wrong when someone guesses 90%. $$P(E \mid H)$$ is a _height_ inside one strip, and $$P(H \mid E)$$ is a _share of area_ across both strips. Mixing them up is common enough that it has names (confusion of the inverse, or the prosecutor's fallacy when it happens in a courtroom). The heights tell you how good the test is, but they say nothing about how wide the strips are, and when the disease is rare the width wins.

## Testing twice

So what do you do after a positive result? Get tested again. If the second test also comes back positive, the odds get multiplied by 10 again, from $$10 : 99$$ to $$100 : 99$$, so $$P(H \mid E_1, E_2) = 100/199 \approx 50\%$$. In the picture, you zoom into the shaded region, then shade and zoom a second time.

There's one catch, and it's the step people forget. Multiplying by the likelihood ratio twice assumes the two results are conditionally independent given whether you're actually sick. If your false positive came from something about you (some other condition the test happens to react to, say), a retest is probably going to pick that up again. Then the second positive tells you a lot less than the formula says, and you shouldn't count it as another factor of 10.
