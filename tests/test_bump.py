# Test Bump Package
# encoding: utf8

# IMPORTS {{{1
from inform import Error
from shlib import Run, cd, rm, to_path, set_prefs
import nestedtext as nt
import arrow


# GLOBALS {{{1
repo_path = to_path('repo')
bump_cfg_path = to_path('.bump.cfg.nt')
info_path = to_path('info.nt')
now = arrow.now()
date = now.format('YYYY-MM-DD')
set_prefs(use_inform=True)

# UTILITIES {{{1
def check_version(major, minor, patch, revision, type, style, version):
    # check bump config file contents
    bump_cfg = nt.load(bump_cfg_path)
    assert bump_cfg['major'] == str(major)
    assert bump_cfg['minor'] == str(minor)
    assert bump_cfg['patch'] == str(patch)
    assert bump_cfg['revision'] == str(revision)
    assert bump_cfg['type'] == type
    assert bump_cfg['style'] == style

    # check version output by bump command
    bump = Run('bump version', 'sOEW')
    assert bump.stdout.strip() == version.strip()

def check_file(version, released=None):
    info = nt.load(info_path)
    assert info['__version__'] == version
    if released is None:
        released = date
    assert info['__released__'] == released


# TESTS {{{1
def test_python():
    try:
        rm(repo_path)
        hg = Run('hg init repo', 'sOEW')
        with cd(repo_path):
            bump = Run('bump initialize python', 'soEW')

            # create file to contain version information
            info_contents = dict(__released__ = '1969-07-20', __version__='0.0')
            nt.dump(info_contents, info_path)

            # update bump config file to include version info file
            bump_cfg = nt.load(bump_cfg_path)
            bump_cfg['files'] = {
                str(info_path): dict(version='__version__', date='__released__')
            }
            nt.dump(bump_cfg, bump_cfg_path)

            # check initial versions of bump config file and info file
            check_file('0.0', '1969-07-20')
            check_version(0, 0, 0, 0, 'release', 'python', '0.0')

            # add files to mercurial and check them in
            hg = Run(f'hg add {bump_cfg_path!s} {info_path!s}', 'sOEW')
            hg = Run(f'hg commit -m update', 'sOEW')

            bump = Run('bump patch', 'soEW')
            check_file('0.0.1')
            check_version(0, 0, 1, 0, 'release', 'python', '0.0.1')

            bump = Run('bump', 'soEW')
            check_file('0.0.2')
            check_version(0, 0, 2, 0, 'release', 'python', '0.0.2')

            bump = Run('bump minor', 'soEW')
            check_file('0.1')
            check_version(0, 1, 0, 0, 'release', 'python', '0.1')

            bump = Run('bump', 'soEW')
            check_file('0.1.1')
            check_version(0, 1, 1, 0, 'release', 'python', '0.1.1')

            bump = Run('bump dev', 'soEW')
            check_file('0.1.2.dev1')
            check_version(0, 1, 2, 1, 'dev', 'python', '0.1.2.dev1')

            bump = Run('bump', 'soEW')
            check_file('0.1.2.dev2')
            check_version(0, 1, 2, 2, 'dev', 'python', '0.1.2.dev2')

            bump = Run('bump alpha', 'soEW')
            check_file('0.1.2a1')
            check_version(0, 1, 2, 1, 'alpha', 'python', '0.1.2a1')

            bump = Run('bump', 'soEW')
            check_file('0.1.2a2')
            check_version(0, 1, 2, 2, 'alpha', 'python', '0.1.2a2')

            bump = Run('bump beta', 'soEW')
            check_file('0.1.2b1')
            check_version(0, 1, 2, 1, 'beta', 'python', '0.1.2b1')

            bump = Run('bump', 'soEW')
            check_file('0.1.2b2')
            check_version(0, 1, 2, 2, 'beta', 'python', '0.1.2b2')

            bump = Run('bump rc', 'soEW')
            check_file('0.1.2rc1')
            check_version(0, 1, 2, 1, 'rc', 'python', '0.1.2rc1')

            bump = Run('bump', 'soEW')
            check_file('0.1.2rc2')
            check_version(0, 1, 2, 2, 'rc', 'python', '0.1.2rc2')

            bump = Run('bump release', 'soEW')
            check_file('0.1.2')
            check_version(0, 1, 2, 0, 'release', 'python', '0.1.2')

            bump = Run('bump post', 'soEW')
            check_file('0.1.2.post1')
            check_version(0, 1, 2, 1, 'post', 'python', '0.1.2.post1')

            bump = Run('bump post', 'soEW')
            check_file('0.1.2.post2')
            check_version(0, 1, 2, 2, 'post', 'python', '0.1.2.post2')

            bump = Run('bump', 'soEW')
            check_file('0.1.2.post3')
            check_version(0, 1, 2, 3, 'post', 'python', '0.1.2.post3')

            bump = Run('bump release', 'sOEW1')
            assert bump.stdout.strip() == "bump error: release: no longer available."
            assert bump.status == 1
            check_file('0.1.2.post3')
            check_version(0, 1, 2, 3, 'post', 'python', '0.1.2.post3')

            bump = Run('bump minor dev', 'soEW')
            check_file('0.2.dev1')
            check_version(0, 2, 0, 1, 'dev', 'python', '0.2.dev1')

            bump = Run('bump dev', 'soEW')
            check_file('0.2.dev2')
            check_version(0, 2, 0, 2, 'dev', 'python', '0.2.dev2')

            bump = Run('bump', 'soEW')
            check_file('0.2.dev3')
            check_version(0, 2, 0, 3, 'dev', 'python', '0.2.dev3')

            bump = Run('bump alpha', 'soEW')
            check_file('0.2a1')
            check_version(0, 2, 0, 1, 'alpha', 'python', '0.2a1')

            bump = Run('bump post', 'sOEW1')
            assert bump.stdout.strip() == "bump error: not yet released."
            assert bump.status == 1
            check_file('0.2a1')
            check_version(0, 2, 0, 1, 'alpha', 'python', '0.2a1')

            bump = Run('bump minor rc', 'soEW')
            check_file('0.3rc1')
            check_version(0, 3, 0, 1, 'rc', 'python', '0.3rc1')

            bump = Run('bump', 'soEW')
            check_file('0.3rc2')
            check_version(0, 3, 0, 2, 'rc', 'python', '0.3rc2')

            bump = Run('bump release', 'soEW')
            check_file('0.3')
            check_version(0, 3, 0, 0, 'release', 'python', '0.3')

            bump = Run('bump post', 'soEW')
            check_file('0.3.post1')
            check_version(0, 3, 0, 1, 'post', 'python', '0.3.post1')

            bump = Run('bump', 'soEW')
            check_file('0.3.post2')
            check_version(0, 3, 0, 2, 'post', 'python', '0.3.post2')

            bump = Run('bump patch', 'soEW')
            check_file('0.3.1')
            check_version(0, 3, 1, 0, 'release', 'python', '0.3.1')

            bump = Run('bump post', 'soEW')
            check_file('0.3.1.post1')
            check_version(0, 3, 1, 1, 'post', 'python', '0.3.1.post1')

            bump = Run('bump alpha', 'sOEW1')
            assert bump.stdout.strip() == "bump error: alpha: no longer available."
            assert bump.status == 1
            check_file('0.3.1.post1')
            check_version(0, 3, 1, 1, 'post', 'python', '0.3.1.post1')

            bump = Run('bump patch', 'soEW')
            check_file('0.3.2')
            check_version(0, 3, 2, 0, 'release', 'python', '0.3.2')

            bump = Run('bump post', 'soEW')
            check_file('0.3.2.post1')
            check_version(0, 3, 2, 1, 'post', 'python', '0.3.2.post1')

            bump = Run('bump beta', 'sOEW1')
            assert bump.stdout.strip() == "bump error: beta: no longer available."
            assert bump.status == 1
            check_file('0.3.2.post1')
            check_version(0, 3, 2, 1, 'post', 'python', '0.3.2.post1')

            bump = Run('bump release', 'sOEW1')
            assert bump.stdout.strip() == "bump error: release: no longer available."
            assert bump.status == 1
            check_file('0.3.2.post1')
            check_version(0, 3, 2, 1, 'post', 'python', '0.3.2.post1')

            bump = Run('bump major', 'soEW')
            check_file('1.0')
            check_version(1, 0, 0, 0, 'release', 'python', '1.0')

    except Error as e:
        print('STDOUT:', e.stdout)
        print('STDERR:', e.stderr)
        print('STATUS:', e.status)
        raise

def test_semver():
    try:
        rm(repo_path)
        hg = Run('hg init repo', 'sOEW')
        with cd(repo_path):
            bump = Run('bump initialize semver', 'soEW')

            # create file to contain version information
            info_contents = dict(__released__ = '1969-07-20', __version__='0.0.0')
            nt.dump(info_contents, info_path)

            # update bump config file to include version info file
            bump_cfg = nt.load(bump_cfg_path)
            bump_cfg['files'] = {
                str(info_path): dict(version='__version__', date='__released__')
            }
            nt.dump(bump_cfg, bump_cfg_path)

            # check initial versions of bump config file and info file
            check_version(0, 0, 0, 0, 'release', 'semver', '0.0.0')
            check_file('0.0.0', '1969-07-20')

            # add files to mercurial and check them in
            hg = Run(f'hg add {bump_cfg_path!s} {info_path!s}', 'sOEW')
            hg = Run(f'hg commit -m update', 'sOEW')

            bump = Run('bump patch', 'soEW')
            check_file('0.0.1')
            check_version(0, 0, 1, 0, 'release', 'semver', '0.0.1')

            bump = Run('bump', 'soEW')
            check_file('0.0.2')
            check_version(0, 0, 2, 0, 'release', 'semver', '0.0.2')

            bump = Run('bump minor', 'soEW')
            check_file('0.1.0')
            check_version(0, 1, 0, 0, 'release', 'semver', '0.1.0')

            bump = Run('bump', 'soEW')
            check_file('0.1.1')
            check_version(0, 1, 1, 0, 'release', 'semver', '0.1.1')

            bump = Run('bump dev', 'soEW')
            check_file('0.1.2-dev.1')
            check_version(0, 1, 2, 1, 'dev', 'semver', '0.1.2-dev.1')

            bump = Run('bump', 'soEW')
            check_file('0.1.2-dev.2')
            check_version(0, 1, 2, 2, 'dev', 'semver', '0.1.2-dev.2')

            bump = Run('bump alpha', 'soEW')
            check_file('0.1.2-alpha.1')
            check_version(0, 1, 2, 1, 'alpha', 'semver', '0.1.2-alpha.1')

            bump = Run('bump', 'soEW')
            check_file('0.1.2-alpha.2')
            check_version(0, 1, 2, 2, 'alpha', 'semver', '0.1.2-alpha.2')

            bump = Run('bump beta', 'soEW')
            check_file('0.1.2-beta.1')
            check_version(0, 1, 2, 1, 'beta', 'semver', '0.1.2-beta.1')

            bump = Run('bump', 'soEW')
            check_file('0.1.2-beta.2')
            check_version(0, 1, 2, 2, 'beta', 'semver', '0.1.2-beta.2')

            bump = Run('bump rc', 'soEW')
            check_file('0.1.2-rc.1')
            check_version(0, 1, 2, 1, 'rc', 'semver', '0.1.2-rc.1')

            bump = Run('bump', 'soEW')
            check_file('0.1.2-rc.2')
            check_version(0, 1, 2, 2, 'rc', 'semver', '0.1.2-rc.2')

            bump = Run('bump release', 'soEW')
            check_file('0.1.2')
            check_version(0, 1, 2, 0, 'release', 'semver', '0.1.2')

            bump = Run('bump post', 'soEW')
            check_file('0.1.2-post.1')
            check_version(0, 1, 2, 1, 'post', 'semver', '0.1.2-post.1')

            bump = Run('bump post', 'soEW')
            check_file('0.1.2-post.2')
            check_version(0, 1, 2, 2, 'post', 'semver', '0.1.2-post.2')

            bump = Run('bump', 'soEW')
            check_file('0.1.2-post.3')
            check_version(0, 1, 2, 3, 'post', 'semver', '0.1.2-post.3')

            bump = Run('bump release', 'sOEW1')
            assert bump.stdout.strip() == "bump error: release: no longer available."
            assert bump.status == 1
            check_file('0.1.2-post.3')
            check_version(0, 1, 2, 3, 'post', 'semver', '0.1.2-post.3')

            bump = Run('bump minor dev', 'soEW')
            check_file('0.2.0-dev.1')
            check_version(0, 2, 0, 1, 'dev', 'semver', '0.2.0-dev.1')

            bump = Run('bump dev', 'soEW')
            check_file('0.2.0-dev.2')
            check_version(0, 2, 0, 2, 'dev', 'semver', '0.2.0-dev.2')

            bump = Run('bump', 'soEW')
            check_file('0.2.0-dev.3')
            check_version(0, 2, 0, 3, 'dev', 'semver', '0.2.0-dev.3')

            bump = Run('bump alpha', 'soEW')
            check_file('0.2.0-alpha.1')
            check_version(0, 2, 0, 1, 'alpha', 'semver', '0.2.0-alpha.1')

            bump = Run('bump post', 'sOEW1')
            assert bump.stdout.strip() == "bump error: not yet released."
            assert bump.status == 1
            check_file('0.2.0-alpha.1')
            check_version(0, 2, 0, 1, 'alpha', 'semver', '0.2.0-alpha.1')

            bump = Run('bump minor rc', 'soEW')
            check_file('0.3.0-rc.1')
            check_version(0, 3, 0, 1, 'rc', 'semver', '0.3.0-rc.1')

            bump = Run('bump', 'soEW')
            check_file('0.3.0-rc.2')
            check_version(0, 3, 0, 2, 'rc', 'semver', '0.3.0-rc.2')

            bump = Run('bump release', 'soEW')
            check_file('0.3.0')
            check_version(0, 3, 0, 0, 'release', 'semver', '0.3.0')

            bump = Run('bump post', 'soEW')
            check_file('0.3.0-post.1')
            check_version(0, 3, 0, 1, 'post', 'semver', '0.3.0-post.1')

            bump = Run('bump', 'soEW')
            check_file('0.3.0-post.2')
            check_version(0, 3, 0, 2, 'post', 'semver', '0.3.0-post.2')

            bump = Run('bump patch', 'soEW')
            check_file('0.3.1')
            check_version(0, 3, 1, 0, 'release', 'semver', '0.3.1')

            bump = Run('bump post', 'soEW')
            check_file('0.3.1-post.1')
            check_version(0, 3, 1, 1, 'post', 'semver', '0.3.1-post.1')

            bump = Run('bump alpha', 'sOEW1')
            assert bump.stdout.strip() == "bump error: alpha: no longer available."
            assert bump.status == 1
            check_file('0.3.1-post.1')
            check_version(0, 3, 1, 1, 'post', 'semver', '0.3.1-post.1')

            bump = Run('bump patch', 'soEW')
            check_file('0.3.2')
            check_version(0, 3, 2, 0, 'release', 'semver', '0.3.2')

            bump = Run('bump post', 'soEW')
            check_file('0.3.2-post.1')
            check_version(0, 3, 2, 1, 'post', 'semver', '0.3.2-post.1')

            bump = Run('bump beta', 'sOEW1')
            assert bump.stdout.strip() == "bump error: beta: no longer available."
            assert bump.status == 1
            check_file('0.3.2-post.1')
            check_version(0, 3, 2, 1, 'post', 'semver', '0.3.2-post.1')

            bump = Run('bump release', 'sOEW1')
            assert bump.stdout.strip() == "bump error: release: no longer available."
            assert bump.status == 1
            check_file('0.3.2-post.1')
            check_version(0, 3, 2, 1, 'post', 'semver', '0.3.2-post.1')

            bump = Run('bump major', 'soEW')
            check_file('1.0.0')
            check_version(1, 0, 0, 0, 'release', 'semver', '1.0.0')

    except Error as e:
        print('STDOUT:', e.stdout)
        print('STDERR:', e.stderr)
        print('STATUS:', e.status)
        raise

