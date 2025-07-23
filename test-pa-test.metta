; Minimal py-atom test
!(bind! pystr (py-atom str))
!(assertEqual (pystr 123) "123") 