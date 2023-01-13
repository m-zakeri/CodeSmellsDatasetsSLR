import pandas as pd


class Exclusion:

    def checkTitle(self, df, Repo, title_index):
        Repo_Titles = list(df.iloc[:, title_index])
        smellTitles = list()
        for title in Repo_Titles:
            print(title)
            title = str(title).lower()
            if 'smell' in title or 'anti pattern' in title or 'antipattern' in title or 'anti-pattern' in title:
                smellTitles.append(title)
        df = pd.DataFrame(smellTitles, columns=['Title'])
        df.to_csv('Result/Separate/' + Repo + '_hitTitles.csv', index=False)
        return df

    def checkAbstrack(self, df, Repo, title_index, abstract_index):
        Repo_Title = list(df.iloc[:, title_index])
        Repo_Abstract = list(df.iloc[:, abstract_index])
        hitAbstract = list()
        for index in range(len(Repo_Abstract)):
            key = str(Repo_Abstract[index]).lower()
            if 'smell' in key or 'smells' in key \
                    or 'anti pattern' in key or 'anti patterns' in key \
                    or 'antipattern' in key or 'antipatterns' in key \
                    or 'anti-pattern' in key or 'anti-patterns' in key \
                    or 'design flaw' in key or 'design flaws' in key:
                if 'dataset' in key or 'datasets' in key \
                        or 'data set' in key or 'data sets' in key \
                        or 'data-set' in key or 'data-sets' in key \
                        or 'machine learning' in key or 'machine learnings' in key \
                        or 'detect' in key or 'detection' in key \
                        or 'huristic' in key or 'huristics' in key:
                    hitAbstract.append(str(Repo_Title[index]).lower())
        df = pd.DataFrame(hitAbstract, columns=['Title'])
        df.to_csv('Result/Separate/' + Repo + '_hitAbstract.csv', index=False)
        return df

    def checkKeywords(self, df, Repo, title_index, keyword_index):
        Repo_Title = list(df.iloc[:, title_index])
        Repo_Keywords = list(df.iloc[:, keyword_index])
        hitKeywords = list()
        for index in range(len(Repo_Keywords)):
            key = str(Repo_Keywords[index]).lower()
            if 'smell' in key or 'smells' in key \
                    or 'anti pattern' in key or 'anti patterns' in key \
                    or 'antipattern' in key or 'antipatterns' in key \
                    or 'anti-pattern' in key or 'anti-patterns' in key \
                    or 'design flaw' in key or 'design flaws' in key:
                if 'dataset' in key or 'datasets' in key \
                        or 'data set' in key or 'data sets' in key \
                        or 'data-set' in key or 'data-sets' in key \
                        or 'machine learning' in key or 'machine learnings' in key \
                        or 'detect' in key or 'detection' in key \
                        or 'heuristic' in key or 'heuristic' in key:
                    hitKeywords.append(str(Repo_Title[index]).lower())
        df = pd.DataFrame(hitKeywords, columns=['Title'])
        df.to_csv('Result/Separate/' + Repo + '_hitKeywords.csv', index=False)
        return df

    def EC5(self, parameters_input):
        Repo_Result = list()
        for repo_index in parameters_input:
            repo_df = pd.read_csv('RepositoriesOutput/' + repo_index[0] + '.csv')
            if repo_index[0] == 'Springer':
                Title_df = self.checkTitle(repo_df, repo_index[0], repo_index[1])
                Abstract_df = pd.DataFrame()
                Keywords_df = pd.DataFrame()
            else:
                Title_df = self.checkTitle(repo_df, repo_index[0], repo_index[1])
                Abstract_df = self.checkAbstrack(repo_df, repo_index[0], repo_index[1], repo_index[2])
                Keywords_df = self.checkKeywords(repo_df, repo_index[0], repo_index[1], repo_index[3])
            combine_df = (pd.concat([Title_df, Abstract_df, Keywords_df], ignore_index=True))
            unique_df = combine_df.drop_duplicates(subset='Title', keep='first', inplace=False, ignore_index=True)
            unique_df.to_csv('Result/Separate/' + repo_index[0] + '_Combined' + '.csv', index=False)
            Repo_Result.append(unique_df)
        Passed_df = (pd.concat(Repo_Result, ignore_index=True))
        Passed_df.to_csv('Result/EC5_Passed.csv', index=False)
        return Passed_df

    def EC1(self, df):
        EC1Passed_df = df.drop_duplicates(subset='Title', keep='first', inplace=False, ignore_index=True)
        EC1Passed_df.to_csv('Result/EC1_Passed.csv', index=False)

    def execute(self):
        parameters_input = [['IEEE', 0, 10, 16],
                            ['ACM', 2, 17, 18],
                            ['ScienceDirect', 3, 16, 17],
                            ['Scopus', 2, 16, 17],
                            ['Springer', 0]]

        EC5Passed_df = self.EC5(parameters_input)
        self.EC1(EC5Passed_df)


if __name__ == '__main__':
    Exclusion().execute()
