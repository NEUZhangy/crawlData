from github import Github
import pprint
import time

class GitRepo:
    url = ""
    name = ""

    def __init__(self, url, name):
        self.url = url
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"git_url: {self.url}, git_name: {self.name}"

g = Github("your key")

# filter is for the specific package name
def crawl(q, pom_filter):
    res = g.search_code(query=f"{q} language:Java")
    count = 0
    pages = res.totalCount // 30 + 1
    print("total pages: ", pages)
    repo_list = set()
    for i in range(0, pages):
        repos = res.get_page(i)
        for x in repos:
            git_repo = GitRepo(url=x.repository.git_url, name=x.repository.full_name)
            try:
                pom_xml = view_raw_content(git_repo)
                if pom_filter in pom_xml and '2.1.1' > pom_xml.split('<version>')[-1].split('</version>')[0]:
                    repo_list.add(git_repo)
            except:
                pass
        print(i)
        time.sleep(60)

    print_repo(repo_list)
    return repo_list

def view_raw_content(git_repo):
    repo = g.get_repo(git_repo.name)
    contents = repo.get_contents("pom.xml")
    return contents.decoded_content.decode('utf-8')
def print_repo(repo_list):
    print("### REPO LIST ###")
    for repo in repo_list:
        print(repo)

if __name__ == "__main__":
    keywords = ['org.dom4j']
    for k in keywords:
        repo_list = crawl(k, "dom4j")