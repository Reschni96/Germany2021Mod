import re

question_regex = re.compile(r'^(E?Q)(\d+):\s*')  # Modified regex to match question lines
answer_regex = re.compile(r'.*A(\d+): (.*)')  # Regular expression to match answer lines
feedback_regex = re.compile(r'F(\d+): (.*)')  # Regular expression to match feedback lines

candidate = 78
pk_questions = 719  # Starting value for pk for questions
pk_answers = 3999  # Starting value for pk for answers
pk_feedback = 4999  # Starting value for pk for feedback

pk_eq_questions = 800  # Starting value for pk for EQ type questions
pk_eq_answers = 4500  # Starting value for pk for EQ type answers
pk_eq_feedback = 5500  # Starting value for pk for EQ type feedback

processing_answers = False
processing_feedback = False
last_question_type = None  # Variable to track the type of the last question processed

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
                question_type = question_match.group(1)
                question_number = question_match.group(2)  # Added to capture the question number
                last_question_type = question_type
                if processing_answers:
                    # We've reached a new question, so all answers for the last question have been processed
                    processing_answers = False
                    if question_type == 'Q':
                        pk_questions += 1
                    else:
                        pk_eq_questions += 1

                description = line[question_match.end():].strip()
                description = description.replace('"', '\\"')  # Escape any quotation marks
                pk = pk_questions if question_type == 'Q' else pk_eq_questions
                out_questions.write(
                    '{{\\"model\\": \\"campaign_trail.question\\", \\"pk\\": {}, \\"fields\\": {{\\"priority\\": 1, \\"description\\": \\"{}\\", \\"likelihood\\": 1.0, \\"question_number\\": \\"{}\\"}}}}, '.format(
                        pk, description, question_number))  # Added question_number to JSON

            elif answer_match:
                processing_answers = True
                if processing_feedback:
                    # We've reached a new answer, so all feedback for the last answer have been processed
                    processing_feedback = False
                    if last_question_type == 'Q':
                        pk_answers += 1
                    else:
                        pk_eq_answers += 1

                description = answer_match.group(2).strip()
                description = description.replace('"', '\\\\\\"')
                pk = pk_answers if last_question_type == 'Q' else pk_eq_answers
                question_pk = pk_questions if last_question_type == 'Q' else pk_eq_questions
                out_answers.write('{{\\"model\\": \\"campaign_trail.answer\\", \\"pk\\": {}, \\"fields\\": {{\\"question\\": {}, \\"description\\": \\"{}\\"}}}}, '.format(pk, question_pk, description))

            elif feedback_match:
                processing_feedback = True
                feedback = feedback_match.group(2).strip()
                feedback = feedback.replace('"', '\\"')
                pk = pk_feedback if last_question_type == 'Q' else pk_eq_feedback
                answer_pk = pk_answers if last_question_type == 'Q' else pk_eq_answers
                out_feedback.write('{{\\"model\\": \\"campaign_trail.answer_feedback\\", \\"pk\\": {}, \\"fields\\": {{\\"answer\\": {}, \\"candidate\\": {}, \\"answer_feedback\\": \\"{}\\"}}}}, '.format(pk, answer_pk, candidate, feedback))
                if last_question_type == 'Q':
                    pk_feedback += 1
                else:
                    pk_eq_feedback += 1

        # Remove the last two characters from each output file
        for outfile in [out_questions, out_answers, out_feedback]:
            size = outfile.tell()
            outfile.seek(size - 2)
            outfile.truncate()

except IOError as e:
    print(f"An error occurred: {e}")
