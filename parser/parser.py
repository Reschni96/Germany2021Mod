import re

question_regex = re.compile(r'^Q(\d+):\s*')  # Regular expression to match question lines

candidate = 78
pk = 717  # Starting value for pk
question_initial = pk

with open('input.txt', 'r', encoding='utf-8') as infile, open('output_questions.txt', 'w', encoding='utf-8') as outfile:
    for line in infile:
        # Check if the line contains a question
        question_match = question_regex.match(line)
        if question_match:
            # Extract the question number and description from the line
            description = line[question_match.end():].strip()

            # Write the question data to the output file in the desired format
            outfile.write('{{\\"model\\": \\"campaign_trail.question\\", \\"pk\\": {}, \\"fields\\": {{\\"priority\\": 1, \\"description\\": \\"{}\\", \\"likelihood\\": 1.0}}}}, '.format(pk, description))

            # Increment the pk value for the next question
            pk += 1

    size = outfile.tell()  # get the current position (i.e., end of file)
    outfile.seek(size - 2)  # move the cursor two positions back from the end
    outfile.truncate()  # remove the last two characters

# Open input and output files for answers
with open('input.txt', 'r', encoding='utf-8') as infile, open('output_answers.txt', 'w', encoding='utf-8') as outfile:
    pk = 4000  # Starting pk value
    initial_answer = pk
    question = question_initial-1  # Starting question value

    # Loop through input file line by line
    for line in infile:
        # Match pk, question, and description using regular expressions
        question_match = re.match(question_regex, line)
        description_match = re.match(r'.*A(\d+): (.*)', line)

        # If question match found, increment question
        if question_match:
            question = question + 1  # Increment question

        # If description match found, write to output file
        elif description_match:
            outfile.write('{{\\"model\\": \\"campaign_trail.answer\\", \\"pk\\": {}, \\"fields\\": {{'.format(pk))
            description = description_match.group(2).strip()  # Extract description text and remove leading/trailing whitespace
            outfile.write('\\"question\\": {}, \\"description\\": \\"{}\\"}}'.format(question, description))
            outfile.write('}, ')
            pk = pk + 1
    size = outfile.tell()  # get the current position (i.e., end of file)
    outfile.seek(size - 2)  # move the cursor two positions back from the end
    outfile.truncate()  # remove the last two characters

# Open input and output files
with open('input.txt', 'r', encoding='utf-8') as infile, open('output_feedback.txt', 'w', encoding='utf-8') as outfile:
    pk = 5000  # Starting pk value
    answer = initial_answer  # Starting answer value

    # Loop through input file line by line
    for line in infile:

        feedback_match = re.match(r'F(\d+): (.*)', line)

        # If feedback match found, write to output file
        if feedback_match:
            outfile.write('{{\\"model\\": \\"campaign_trail.answer_feedback\\", \\"pk\\": {}, \\"fields\\": {{'.format(pk))
            feedback = feedback_match.group(2).strip()  # Extract feedback text and remove leading/trailing whitespace
            outfile.write('\\"answer\\": {}, \\"candidate\\": {}, \\"answer_feedback\\": \\"{}\\"}}'.format(answer, candidate, feedback))
            outfile.write('}, ')
            pk = pk + 1
            answer = answer + 1
    size = outfile.tell()  # get the current position (i.e., end of file)
    outfile.seek(size - 2)  # move the cursor two positions back from the end
    outfile.truncate()  # remove the last two characters


