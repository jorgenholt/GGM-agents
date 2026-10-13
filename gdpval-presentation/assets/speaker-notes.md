# Speaker notes: GDPval presentation

Planned time per slide in brackets. Jørgen presents slides 1–9, Save presents 10–17.

## 1. Can AI do an expert's job? (0.3 min · Jørgen · The paper)
*Purpose:* Name the paper and set up the one question the talk answers

- Introduce yourselves: Jørgen and Save, project thesis on AI agents for the Global Gas Model.
- The paper: GDPval, by Patwardhan and colleagues at OpenAI, ICLR 2026.
- One question runs through the talk: can AI actually do the work of an experienced professional?

*Transition:* Why this is a different question from what most benchmarks ask

## 2. Exams vs. jobs (0.4 min · Jørgen · The paper)
*Purpose:* Give the core idea in one line, then a non-generic roadmap

- Most AI benchmarks are exams: hard questions with one right answer.
- GDPval asks models to produce what people are paid for: a legal memo, a spreadsheet, a slide deck.
- Roadmap: what they measured, the 2025 results, what changed in the year since, a live test in our own field, and what it means for our thesis.

*Transition:* First, where this sits in the literature

## 3. Why another benchmark? (0.3 min · Jørgen · The paper)
*Purpose:* Place GDPval against the three existing ways of measuring AI's economic impact

- Economic statistics are real but lag by years.
- Exam benchmarks measure reasoning, not deliverables.
- SWE-Lancer measures paid work, but only in software. GDPval fills the gap across the economy.

*Transition:* So what does the dataset look like?

## 4. The dataset (0.35 min · Jørgen · The paper)
*Purpose:* Show the scale and realism of the contribution

- 9 sectors that each make up more than 5% of US GDP, 44 occupations, $3T in wages.
- Experts with 14 years of experience on average wrote 1,320 tasks from their own work; about 7 hours each.
- 220 tasks, including the experts' own answers, are public.

*Transition:* How do you grade work like that?

## 5. How a task is built and graded (0.35 min · Jørgen · The paper)
*Purpose:* Explain blind pairwise grading

- The model and the original expert both produce the deliverable.
- Another expert sees both, unlabelled, and picks the better one.
- No answer key: the score is expert preference, and experts agree with each other only 71% of the time.

*Transition:* So how close did AI get?

## 6. Headline results (2025) (0.5 min · Jørgen · The paper)
*Purpose:* Deliver the paper's headline number and trend

- Win plus tie rate against the human expert; 50% means parity.
- The best model, Claude Opus 4.1, reached 47.6%.
- Claude won on formatting; GPT-5 on accuracy. Performance rose roughly linearly over time.

*Transition:* The headline hides where things break

## 7. Where the models break (2025) (0.5 min · Jørgen · The paper)
*Purpose:* Show the limits behind the headline number

- Longer tasks: win rates fall with task length.
- Speed: 90× faster becomes about 1.4× once an expert reviews and redoes failures.
- Most losses came from not following instructions; a few were catastrophic.

*Transition:* That was 2025. What happened since?

## 8. From 48% to 85% (0.7 min · Jørgen · One year later)
*Purpose:* Show how fast the paper's headline number became outdated

- Same metric as the paper, all from OpenAI's launch announcements.
- From Opus 4.1 (released August 2025) at 47.6% to GPT-5.2 in December 2025: 70.9%. GPT-5.4 in March: 83%, and it beats the expert outright on 71% of tasks. GPT-5.5 in April: 84.9%.
- OpenAI also graded Claude and Gemini: Opus 4.5 at 60% and Gemini 3 at 54% in December, Opus 4.7 at 80% and Gemini 3.1 at 67% in April.
- Then the series stops: from GPT-5.6, OpenAI reports a different version, and GPT-6 Astra reports none. xAI and DeepSeek never published this test.

*Transition:* But which of these numbers are actually comparable?

## 9. Same name, three tests (0.6 min · Jørgen · One year later)
*Purpose:* Separate comparable numbers from look-alikes

- Level 1 is the paper's test: blind expert grading, same metric. OpenAI's GPT-5 number matches the paper, so the method looks unchanged. It also includes OpenAI's now-removed leaderboard with Opus 4.5, Sonnet 4.5 and Gemini 3.
- Level 2 is GDPval-AA from Artificial Analysis: same tasks, but an AI judge ranks models against each other. That's what Anthropic, Google, xAI and DeepSeek report, and OpenAI since GPT-5.6.
- Level 3: new benchmarks that borrow the name.
- Even level 1 is self-reported, and the public tasks could have leaked into training data.

*Transition:* Hand over to Save: so which jobs actually improved?

## 10. Jobs: 2025 vs. Dec 2025 (0.7 min · Save · One year later)
*Purpose:* Show which kinds of work improved, using OpenAI's own per-occupation data

- OpenAI ran a public GDPval leaderboard with results per occupation. It stopped updating in December 2025 and was taken offline in 2026; we recovered the data from the Internet Archive.
- Grey is the best model of Aug–Sep 2025 (Claude Opus 4.1, GPT-5), black the best model of Dec 2025. Same expert grading, about four months apart.
- Grey is a period, not a day: the Opus 4.1 era, Aug 5 to Sep 28, gives the same bars on any date. Opus 4.1 led for under eight weeks, until Sonnet 4.5 on Sep 29.
- If asked about the 'four months': release to release (Aug 5 to Dec 11) and midpoint to midpoint of each model's reign both give about four months. Mixing them, e.g. the middle of Opus 4.1's reign to GPT-5.2's release, would shorten it unfairly.
- Accountants went from 24% to 56%, engineers from around 20-27% to 60%, nurses from 36% to 87%: the precise, numbers-heavy work that was weakest in 2025.
- Still behind: film editors, financial managers, concierges. Only 5 tasks per occupation, so look at the pattern, not single bars.

*Transition:* Outside GDPval, the same shift shows up in other tests

## 11. Did the type of work change? (0.5 min · Save · One year later)
*Purpose:* Answer the task-type question honestly with the evidence available

- In 2025, models lost on instruction-following and accuracy, and miscalculations were a named failure.
- Since then, the areas vendors advertise are exactly those: financial spreadsheet models went from 59% to 89% on OpenAI's internal test, and hard math from 31% to 52%.
- Within GDPval itself, models now beat experts outright, not just tie.
- This matches the leaderboard: accountants 24% to 56%. After December 2025 there is no per-job GDPval data at all.

*Transition:* Which brings us to our overall view of the paper

## 12. Our view (0.7 min · Save · Discussion & thesis)
*Purpose:* Give a balanced critique: two strengths, four weaknesses

- Strengths: realistic tasks with blind peer grading, and an honest cost analysis.
- Biggest weakness, as we just saw: it dated within months, and the number is close to its ceiling.
- Tasks are fully specified and one-shot. OpenAI evaluates OpenAI, and it removed the per-job leaderboard once it stopped updating it. And preference is not correctness.

*Transition:* Enough numbers: let's test today's best model live, in our own field.

## 13. Live test: be the grader (0.8 min · Save · Live test)
*Purpose:* Let the audience and Franziska grade blind, as GDPval graders did

- Frame it: we've seen the numbers, so now we test the newest Claude live, on a question from our own field, with our supervisor as the expert grader.
- Read the task aloud: March 2015, OPEC has just refused to cut output. Does OPEC actually act as a cartel?
- One answer is from an energy economist, one from an AI. Don't say who.
- Give the room about 45 seconds, then ask for hands: which is better?
- Then ask Franziska, as our expert grader, which one she prefers and why.
- *Interaction:* Room votes by show of hands, then Franziska gives her verdict
- *Cue:* Ask Franziska before the talk if she is happy to judge a short text live, without saying what it is

*Transition:* Then reveal

## 14. Live test: the reveal (0.4 min · Save · Live test)
*Purpose:* Connect the room's and the expert's verdicts to the paper's grading problem

- A is Claude Opus 5.5 with high reasoning: fresh chat, first answer. The exact prompt is on screen: same date, role, length and question as the authors, no hints. B is Franziska, from her 2015 DIW Roundup with Daniel Huppmann.
- Compare the room with the expert: did they agree? In the paper, experts agree with each other only 71% of the time.
- Method, if asked: the paragraph was chosen before Claude was run, because it answers the question directly; only a web address was removed.

*Transition:* This is exactly the kind of expert work our thesis is about.

## 15. Our thesis (0.5 min · Save · Discussion & thesis)
*Purpose:* Present the thesis title, supervisor and idea in one picture

- Preliminary title: Pipelines & Prompts: AI Agents for the Global Gas Model. Supervisor: Franziska Holz.
- GGM is DIW Berlin's equilibrium model of world gas markets, with market power; scenarios mean editing large Excel workbooks.
- GGM stays untouched in the core; agents prepare, check and explain; the analyst stays in charge.
- The analyst sees and approves every change the agent wants to make to the input files before the model runs.

*Transition:* What does GDPval teach us for that design?

## 16. Four lessons for GGM (0.5 min · Save · Discussion & thesis)
*Purpose:* Make the link between the paper and the thesis explicit

- Decompose, because long tasks fail more. Specify, because models struggle with missing context.
- Verify, because self-checks help. Evaluate the GDPval way, because GGM parameters have no ground truth.
- And the gap: what GDPval excludes is exactly what GGM is.

*Transition:* To sum up

## 17. Conclusion (0.3 min · Save · Discussion & thesis)
*Purpose:* Close with one memorable line and three takeaways

- Capable on the task, not yet on the job.
- Past expert level on well-specified work within a year. The hard part is ambiguity, length and judgement.
- That is where we design agents that prepare, check and explain. Thank you, questions?

*Transition:* Open for questions
