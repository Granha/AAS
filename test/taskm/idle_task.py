from taskm.idle_task import IdleTask

import unittest

class TestIdleTask(unittest.TestCase):

    def testInteralState(self):        
        idleTask = IdleTask()

        self.assertEqual(idleTask.getName(), "Idle")
        self.assertTrue(idleTask.isIdleTask())
        self.assertEqual(idleTask.getPriority(), -1)
    # testInteralState
    
# TestTask

if __name__ == '__main__':
    unittest.main()
