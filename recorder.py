

class ShellRecorder():

    def __init__(self):
        self.records = []
        self.pointer = len(self.records)
        # flag indicates if we are in recorder mode
        self.traverse = False

    def empty(self):
        """
        check if recorder is empty
        """
        if len(self.records) == 0:
            return True
        return False

    def clear(self):
        """
        clear all records and reset status
        """
        self.records.clear()
        self.pointer = len(self.records)
        self.traverse = False

    def status(self):
        """
        check recorder mode
        """
        return self.traverse

    def rewind(self):
        """
        reset recorder state
        """
        # remove temporarily appended user input string
        if self.records:
            self.records.remove(self.records[-1])
        self.pointer = len(self.records)
        self.traverse = False

    def append(self, record):
        """
        append temporarily input command to recorder,
        we can dynamically remove from recorder if needed
        """
        self.records.append(record)

    def commit(self, command):
        """
        Add command to recorder if it is not blank
        If it's the same with the last element in recorder, leave it
        """
        command = command.strip()

        # empty command, no need to add it to recorder
        if not command:
            return

        if self.records and command == self.records[-1]:
            return

        self.records.append(command)
        self.pointer = len(self.records)

    def traverse(self, direction, temporary_input=''):
        if not self.traverse:
            return ''
        if direction == 'up':
            if not self.traverse:
                self.traverse = True
                self.records.append(temporary_input)

            # We have reached the furthest records, no need to move
            if self.pointer == 0:
                return self.records[self.pointer]

            # We have more records to traverse, move to previous one
            self.pointer -= 1
            return self.records[self.pointer]
        elif direction == 'down':
            if self.pointer == len(self.records)-1:
                return self.records[self.pointer]

            self.pointer += 1
            return self.records[self.pointer]
        else:
            pass

    def next(self):
        """
        return next command in recorder list if exists
        """
        # We have come to the last command, don't need to jump
        # to next command, just return it and keep pointer still
        if self.pointer == len(self.records)-1:
            return self.records[self.pointer]

        # jump to next command
        self.pointer += 1
        return self.records[self.pointer]

    def prev(self):
        # prev() gets us into recorder mode if we haven't been in
        if not self.traverse:
            self.traverse = True
        # we've reached the furthest record, just stop here
        if self.pointer == 0:
            return self.records[self.pointer]

        # we have more records to traverse, move to previous one
        self.pointer -= 1
        return self.records[self.pointer]