# Spec for the Fedora AI/ML SIG Agent Skills Library.
# One subpackage per skill plus a metapackage that installs all of
# them. Context: https://forge.fedoraproject.org/ai-ml/skills-library/issues/3
#
# Skills install to the proposed system-level path:
#   /usr/share/agents/skills/<skill-name>/
#
# After installation, point your agent harness at the path, e.g.
# OpenCode: { "skills": { "paths": ["/usr/share/agents/skills"] } }

# Proposed standard system-level skills directory. The path is not
# yet owned by the "filesystem" package, so every skill subpackage
# co-owns the two parent directories; any skill can be installed
# standalone (see the Unowned Directories guidelines).
%global skillsdir %{_datadir}/agents/skills

# One subpackage is generated per skill in this list. Subpackage
# names are "agent-skill-" plus the exact skill directory slug
# (validated in %%check). When a skill is added or removed upstream,
# update this list plus the Requires, %%package and %%files blocks.
%global skill_list fedora-compose-triage fedora-ftbfs-search fedora-packaging meeting-secretary packit-pull-from-upstream-onboarding

Name:           agent-skills
Version:        0.1.0
Release:        1%{?dist}
Summary:        Metapackage installing all Fedora AI/ML SIG Agent Skills

License:        CC-BY-SA-4.0
URL:            https://forge.fedoraproject.org/ai-ml/skills-library
# Fedora Forge (Forgejo) is not covered by the %%forgemeta macros, so
# this follows the "Git Hosting Services" pattern from the SourceURL
# guidelines. Forgejo tag archives extract to a top-level
# "skills-library/" directory. The "#/" fragment names the downloaded
# tarball locally, per the documented workaround for troublesome URLs.
# Verify the tag exists before building:
#   git ls-remote --tags https://forge.fedoraproject.org/ai-ml/skills-library.git
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

# The main package is the metapackage: installing it pulls in every
# skill in the library. Each skill is also individually installable
# as "agent-skill-<skill-name>".
Requires:       agent-skill-fedora-compose-triage
Requires:       agent-skill-fedora-ftbfs-search
Requires:       agent-skill-fedora-packaging
Requires:       agent-skill-meeting-secretary
Requires:       agent-skill-packit-pull-from-upstream-onboarding

%description
The Fedora AI/ML SIG maintains a library of Agent Skills:
self-contained, versioned directories of instructions and reference
material that give AI agents specialized knowledge for Fedora
community workflows.

This metapackage installs every skill in the library to the
system-level path /usr/share/agents/skills/, where each skill lands
in its own directory containing a SKILL.md entry point plus optional
references and assets.

After installation, point your agent harness at the skills path. For
example, in OpenCode:

    { "skills": { "paths": ["/usr/share/agents/skills"] } }


%package -n agent-skill-fedora-compose-triage
Summary:        Agent skill to triage Fedora compose-tracker issues
License:        CC-BY-SA-4.0

%description -n agent-skill-fedora-compose-triage
Staged workflow for investigating FINISHED_INCOMPLETE and DOOMED
composes by running one compose-tracker issue through a fixed
sequence of stages, each producing structured output for the next.


%package -n agent-skill-fedora-ftbfs-search
Summary:        Agent skill to search Bugzilla for Fedora FTBFS/FTI bugs
License:        CC-BY-SA-4.0

%description -n agent-skill-fedora-ftbfs-search
Search Bugzilla for existing Fails To Build From Source (FTBFS) or
Fails To Install (FTI) bugs for packages needing a rebuild.


%package -n agent-skill-fedora-packaging
Summary:        Agent skill for Fedora RPM packaging assistance
License:        CC-BY-SA-4.0

%description -n agent-skill-fedora-packaging
Fedora RPM packaging assistant. Helps create, update, modernize, and
review spec files using the official Fedora Packaging Guidelines.
Use when working on RPM spec files, fedpkg workflows, package
reviews, or packaging questions.


%package -n agent-skill-meeting-secretary
Summary:        Agent skill to turn Fedora Meetbot logs into Markdown posts
License:        CC-BY-SA-4.0

%description -n agent-skill-meeting-secretary
Transform Fedora Meetbot HTML log files into structured Markdown
outputs: Fedora Discussion summary posts and Forgejo ticket comments.


%package -n agent-skill-packit-pull-from-upstream-onboarding
Summary:        Agent skill to onboard packages to Packit pull-from-upstream
License:        CC-BY-SA-4.0

%description -n agent-skill-packit-pull-from-upstream-onboarding
Set up fully automated upstream-release tracking for a Fedora
dist-git package using Packit: new upstream releases are
automatically pulled into dist-git, the spec file is updated, and a
Koji build is triggered.


%prep
# Forgejo tag archives extract to a top-level "skills-library/".
%autosetup -n skills-library


%build
# Data-only package: nothing to compile.


%install
# RPM creates /usr/share/agents/ automatically because the dirs are
# listed as %%dir in every %%files section below.
install -m 0755 -vd %{buildroot}%{skillsdir}
for skill in %{skill_list}; do
    # cp -a preserves the executable bits on bundled asset scripts.
    cp -a "skills/${skill}" "%{buildroot}%{skillsdir}/${skill}"
done


%check
# Guard against packaging drift: every skill must ship a SKILL.md
# whose frontmatter "name" exactly matches its directory slug.
for skill in %{skill_list}; do
    test -f "%{buildroot}%{skillsdir}/${skill}/SKILL.md" \
        || { echo "ERROR: missing SKILL.md for ${skill}" >&2; exit 1; }
    grep -q "^name: ${skill}$" "%{buildroot}%{skillsdir}/${skill}/SKILL.md" \
        || { echo "ERROR: frontmatter name mismatch for ${skill}" >&2; exit 1; }
done


%files
%license LICENSE.txt
%doc README.md
%doc CONTRIBUTING.md


%files -n agent-skill-fedora-compose-triage
%license LICENSE.txt
%dir %{_datadir}/agents
%dir %{skillsdir}
%{skillsdir}/fedora-compose-triage/


%files -n agent-skill-fedora-ftbfs-search
%license LICENSE.txt
%dir %{_datadir}/agents
%dir %{skillsdir}
%{skillsdir}/fedora-ftbfs-search/


%files -n agent-skill-fedora-packaging
%license LICENSE.txt
%dir %{_datadir}/agents
%dir %{skillsdir}
%{skillsdir}/fedora-packaging/


%files -n agent-skill-meeting-secretary
%license LICENSE.txt
%dir %{_datadir}/agents
%dir %{skillsdir}
%{skillsdir}/meeting-secretary/


%files -n agent-skill-packit-pull-from-upstream-onboarding
%license LICENSE.txt
%dir %{_datadir}/agents
%dir %{skillsdir}
%{skillsdir}/packit-pull-from-upstream-onboarding/


%changelog
* Tue Oct 27 2026 Justin Wheeler <jflory7@fedoraproject.org> - 0.1.0-1
- Initial experimental package of the Fedora AI/ML SIG Agent Skills Library
- Package each of the five skills as an individual noarch RPM installed
  under /usr/share/agents/skills/ (ai-ml/skills-library issue #3)
- Main package is a metapackage requiring all five agent-skill-* subpackages
- Build from the first upstream tag v0.1.0
