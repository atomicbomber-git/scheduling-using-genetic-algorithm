import timeslot

t1 = timeslot.timeslots[0]
t2 = timeslot.timeslots[4]

print(t1)
print(t2)
print(t1.overlaps(t2))