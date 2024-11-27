from github_poster.loader.gitlab_loader import GitLabLoader

# Sample GitLab HTML response
SAMPLE_HTML = """
<h4 class="prepend-top-20">
    Contributions for <strong>Nov 26, 2024</strong>
</h4>
<ul class="bordered-list">
    <li>
        <span class="light">
<svg class="s16 gl-vertical-align-text-bottom" data-testid="clock-icon"><use xlink:href="/assets/icons-6d7d4be41eac996c72b30eac2f28399ac8c6eda840a6fe8762fc1b84b30d5a2d.svg#clock"></use></svg>
6:44am
</span>
        pushed new branch
        <strong>
<a href="/shopee/seller-server/open-platform/opservice/-/commits/songjian.li/feature/SPSL-100485/clean_partner_shop_log_tab">songjian.li/feature/SPSL-100485/clean_partner_shop_log_tab</a>
</strong>
        at
        <strong>
<a title="opservice" class="gl-link" href="/shopee/seller-server/open-platform/opservice"><span class="namespace-name">Shopee / seller-server / open-platform / </span><span class="project-name">opservice</span></a>
</strong>
    </li>
    <li>
        <span class="light">
<svg class="s16 gl-vertical-align-text-bottom" data-testid="clock-icon"><use xlink:href="/assets/icons-6d7d4be41eac996c72b30eac2f28399ac8c6eda840a6fe8762fc1b84b30d5a2d.svg#clock"></use></svg>
7:48am
</span>
        pushed to branch
        <strong>
<a href="/shopee/seller-server/seller-platform/notification_api/-/commits/zhichuang.li/feature/SPSL-98966/gas-hspex-support">zhichuang.li/feature/SPSL-98966/gas-hspex-support</a>
</strong>
        at
        <strong>
<a title="notification_api" class="gl-link" href="/shopee/seller-server/seller-platform/notification_api"><span class="namespace-name">Shopee / seller-server / seller-platform / </span><span class="project-name">notification_api</span></a>
</strong>
    </li>
    <li>
        <span class="light">
<svg class="s16 gl-vertical-align-text-bottom" data-testid="clock-icon"><use xlink:href="/assets/icons-6d7d4be41eac996c72b30eac2f28399ac8c6eda840a6fe8762fc1b84b30d5a2d.svg#clock"></use></svg>
7:52am
</span>
        pushed to branch
        <strong>
<a href="/shopee/seller-server/seller-platform/notification_api/-/commits/zhichuang.li/feature/SPSL-98966/gas-hspex-support">zhichuang.li/feature/SPSL-98966/gas-hspex-support</a>
</strong>
        at
        <strong>
<a title="notification_api" class="gl-link" href="/shopee/seller-server/seller-platform/notification_api"><span class="namespace-name">Shopee / seller-server / seller-platform / </span><span class="project-name">notification_api</span></a>
</strong>
    </li>
    <li>
        <span class="light">
<svg class="s16 gl-vertical-align-text-bottom" data-testid="clock-icon"><use xlink:href="/assets/icons-6d7d4be41eac996c72b30eac2f28399ac8c6eda840a6fe8762fc1b84b30d5a2d.svg#clock"></use></svg>
10:13am
</span>
        closed merge request
        <strong>
<a class="has-tooltip" title="[SPSL-94219]: songjian.li/integration_soup_nopfb" href="/shopee/seller-server/open-platform/opservice/-/merge_requests/1207">!1207</a>
</strong>
        at
        <strong>
<a title="opservice" class="gl-link" href="/shopee/seller-server/open-platform/opservice"><span class="namespace-name">Shopee / seller-server / open-platform / </span><span class="project-name">opservice</span></a>
</strong>
    </li>
    <li>
        <span class="light">
<svg class="s16 gl-vertical-align-text-bottom" data-testid="clock-icon"><use xlink:href="/assets/icons-6d7d4be41eac996c72b30eac2f28399ac8c6eda840a6fe8762fc1b84b30d5a2d.svg#clock"></use></svg>
10:14am
</span>
        pushed to branch
        <strong>
<a href="/shopee/seller-server/open-platform/opservice/-/commits/songjian.li/feature/SPSL-94219/integration_soup">songjian.li/feature/SPSL-94219/integration_soup</a>
</strong>
        at
        <strong>
<a title="opservice" class="gl-link" href="/shopee/seller-server/open-platform/opservice"><span class="namespace-name">Shopee / seller-server / open-platform / </span><span class="project-name">opservice</span></a>
</strong>
    </li>
    <li>
        <span class="light">
<svg class="s16 gl-vertical-align-text-bottom" data-testid="clock-icon"><use xlink:href="/assets/icons-6d7d4be41eac996c72b30eac2f28399ac8c6eda840a6fe8762fc1b84b30d5a2d.svg#clock"></use></svg>
10:37am
</span>
        pushed to branch
        <strong>
<a href="/shopee/seller-server/open-platform/opservice/-/commits/songjian.li/feature/SPSL-100485/clean_partner_shop_log_tab">songjian.li/feature/SPSL-100485/clean_partner_shop_log_tab</a>
</strong>
        at
        <strong>
<a title="opservice" class="gl-link" href="/shopee/seller-server/open-platform/opservice"><span class="namespace-name">Shopee / seller-server / open-platform / </span><span class="project-name">opservice</span></a>
</strong>
    </li>
    <li>
        <span class="light">
<svg class="s16 gl-vertical-align-text-bottom" data-testid="clock-icon"><use xlink:href="/assets/icons-6d7d4be41eac996c72b30eac2f28399ac8c6eda840a6fe8762fc1b84b30d5a2d.svg#clock"></use></svg>
10:58am
</span>
        pushed to branch
        <strong>
<a href="/shopee/seller-server/open-platform/opservice/-/commits/songjian.li/feature/SPSL-100485/clean_partner_shop_log_tab">songjian.li/feature/SPSL-100485/clean_partner_shop_log_tab</a>
</strong>
        at
        <strong>
<a title="opservice" class="gl-link" href="/shopee/seller-server/open-platform/opservice"><span class="namespace-name">Shopee / seller-server / open-platform / </span><span class="project-name">opservice</span></a>
</strong>
    </li>
    <li>
        <span class="light">
<svg class="s16 gl-vertical-align-text-bottom" data-testid="clock-icon"><use xlink:href="/assets/icons-6d7d4be41eac996c72b30eac2f28399ac8c6eda840a6fe8762fc1b84b30d5a2d.svg#clock"></use></svg>
11:21am
</span>
        pushed to branch
        <strong>
<a href="/shopee/seller-server/open-platform/opservice/-/commits/songjian.li/feature/SPSL-100485/clean_partner_shop_log_tab">songjian.li/feature/SPSL-100485/clean_partner_shop_log_tab</a>
</strong>
        at
        <strong>
<a title="opservice" class="gl-link" href="/shopee/seller-server/open-platform/opservice"><span class="namespace-name">Shopee / seller-server / open-platform / </span><span class="project-name">opservice</span></a>
</strong>
    </li>
</ul>
"""

def main():
    # Initialize GitLabLoader with sample parameters
    loader = GitLabLoader(
        from_year=2024,
        to_year=2024,
        _type="gitlab",
        gitlab_user_name="test_user",
        base_url="https://gitlab.com",
        session=""
    )
    
    # Test the activity counting
    try:
        activity_count = loader.count_activities_from_html(SAMPLE_HTML)
        print(f"Number of activities found: {activity_count}")
        
        # Test with empty HTML
        empty_count = loader.count_activities_from_html("")
        print(f"Number of activities in empty HTML: {empty_count}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
