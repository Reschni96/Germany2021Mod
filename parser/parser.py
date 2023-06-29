import re

question_regex = re.compile(r'^Q(\d+):\s*')  # Regular expression to match question lines
answer_regex = re.compile(r'.*A(\d+): (.*)')  # Regular expression to match answer lines
feedback_regex = re.compile(r'F(\d+): (.*)')  # Regular expression to match feedback lines

candidate = 77
pk_questions = 717  # Starting value for pk for questions
pk_answers = 4000  # Starting value for pk for answers
pk_feedback = 5000  # Starting value for pk for feedback
processing_answers = False
processing_feedback = False

try:
    with open('input.txt', 'r', encoding='utf-8') as infile, \
         open('output_questions.txt', 'w', encoding='utf-8') as out_questions, \
         open('output_answers.txt', 'w', encoding='utf-8') as out_answers, \
         open('output_feedback.txt', 'w', encoding='utf-8') as out_feedback:

        for line in infile:
            # Check if the line contains a question, an answer, or feedback
            question_match = question_regex.match(line)
            answer_match = answer_regex.match(line)
            feedback_match = feedback_regex.match(line)

            if question_match:
                if processing_answers:
                    # We've reached a new question, so all answers for the last question have been processed
                    processing_answers = False
                    pk_questions += 1

                description = line[question_match.end():].strip()
                description = description.replace('"', '\\"')  # Escape any quotation marks

                out_questions.write(
                    '{{\\"model\\": \\"campaign_trail.question\\", \\"pk\\": {}, \\"fields\\": {{\\"priority\\": 1, \\"description\\": \\"{}\\", \\"likelihood\\": 1.0}}}}, '.format(
                        pk_questions, description))

            elif answer_match:
                processing_answers = True
                if processing_feedback:
                    # We've reached a new answer, so all feedback for the last answer have been processed
                    processing_feedback = False
                    pk_answers += 1

                description = answer_match.group(2).strip()
                description = description.replace('"', '\\"')
                out_answers.write('{{\\"model\\": \\"campaign_trail.answer\\", \\"pk\\": {}, \\"fields\\": {{\\"question\\": {}, \\"description\\": \\"{}\\"}}}}, '.format(pk_answers, pk_questions, description))

            elif feedback_match:
                processing_feedback = True
                feedback = feedback_match.group(2).strip()
                feedback = feedback.replace('"', '\\"')
                out_feedback.write('{{\\"model\\": \\"campaign_trail.answer_feedback\\", \\"pk\\": {}, \\"fields\\": {{\\"answer\\": {}, \\"candidate\\": {}, \\"answer_feedback\\": \\"{}\\"}}}}, '.format(pk_feedback, pk_answers, candidate, feedback))
                pk_feedback += 1

        # Remove the last two characters from each output file
        for outfile in [out_questions, out_answers, out_feedback]:
            size = outfile.tell()
            outfile.seek(size - 2)
            outfile.truncate()

except IOError as e:
    print(f"An error occurred: {e}")
