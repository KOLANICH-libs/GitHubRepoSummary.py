import typing
from warnings import warn

from miniGHAPI.GitHubAPI import Repo

__all__ = ("formatRepoInfo",)

metersToEmoji = {
	"stargazers_count": "⭐",
	"watchers_count": "👁️",
	"subscribers_count": "👂",
	"forks": "🍴",
	"open_issues_count": "🪰",
	"network_count": "🌳",
}

timersToEmoji = {
	"created_at": "+",
	"updated_at": "*",
	"pushed_at": "🫸",
}


def formatRepoInfo(r: Repo, printReadMe: typing.Union[bool, str] = False):
	repoInfo = r.getInfo()

	defaultBranch = repoInfo["default_branch"]
	warningIndicators = ["archived", "disabled"]
	for el in warningIndicators:
		if repoInfo[el]:
			yield "Warning: the repo is " + el

	if repoInfo["description"]:
		yield repoInfo["description"]
	if repoInfo["homepage"]:
		yield repoInfo["homepage"]
	yield " ".join(e + " " + str(repoInfo[k]) for k, e in metersToEmoji.items())
	yield " ".join(e + " " + repoInfo[k] for k, e in timersToEmoji.items())
	if repoInfo["topics"]:
		print("Topics:", ", ".join(repoInfo["description"]))

	def processReadMe(r):
		from GitHubReadMeRender import getAndRenderReadMe

		yield getAndRenderReadMe(r)

	if printReadMe is True:
		yield from processReadMe(r)
	elif printReadMe is None:
		try:
			yield from processReadMe(r)
		except ImportError as ex:
			warn("Libs needed to render ReadMe are not installed" + repr(ex))

	elif isinstance(printReadMe, str):
		yield printReadMe
