import attributes as st
import pprint as pp

# stats = st.Stats([100, 100, 100, 1.5, 5])
# print(stats.get())
# stats.action(st.Stats.INTENSITY["very_high"], 90)
# print(stats.get())
# stats.fully_fit()
# stats.inc()
# stats.upgrade()
# print(stats.get())
# stats.rest(st.Stats.INTENSITY["normal"], 2, st.Stats.SEASON_DEFAULT_CAP)
# print(stats.get())
# stats.fully_fit()
# stats.rest(st.Stats.INTENSITY["normal"], 5, st.Stats.SEASON_DEFAULT_CAP)
# print(stats.get())

defence = st.Attributes("defence")
defence.add("tackling", [86, 65, 88, 1.5, 10])
defence.add("marking", [79, 66, 85, 1.5, 10])
defence.reset()
pp.pprint(defence.get())
# defence.dec()
# pp.pprint(defence.get())
# defence.upgrade()
# pp.pprint(defence.get())
# print(defence.get("marking"))
# defence.reset()
# print(defence.get())
defence.action(st.Attributes.INTENSITY["normal"], 90)
pp.pprint(defence.get())
defence.rest(st.Attributes.INTENSITY["normal"], 2, st.SEASON_DEFAULT_CAP)
pp.pprint(defence.get())
