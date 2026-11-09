You read part of an interview. An analyst asked one future user of a software service a series of questions. You decide, for each question, whether it follows up the answer given just before it.

A question follows up the previous answer when it asks about something that answer said: it asks the speaker to explain, give an example of, say more about, or say why of something the answer mentioned, or it picks up a particular thing the answer named. Wording does not matter; a question can follow up an answer without repeating any of its words.

A question does not follow up the previous answer when it turns to something that answer did not mention, even if the speaker said it in an earlier answer, even if it stays with the same broad subject, and even if it is a good question. A general question that could follow any answer, such as whether there is anything else, does not follow up either.

You receive the pairs of the interview after its first question: for each later question, the answer given just before it, and the question.

Reply with JSON only: an object with one key, "questions", a list with exactly one entry for every pair, in the same order. Each entry has "id", the question's id, and "follow_up", true or false.
