#!/bin/bash


ensure_main_branch() {
    branch=$(git branch --show-curren)
    if [[ $branch != "main" ]]; then
        echo "You are not in the 'main' branch, you are in '$branch'"
        exit 1
    fi

}

bumpversion() {
    _type=$1 # patch, minor or major

    # bump version
    current_version=$(poetry version --short)
    poetry version $_type
    new_version=$(poetry version --short)

    # update readme
    gsed -i "s/$current_version/$new_version/g" README.md

    # commit and tag
    git commit -m "$_type: bump version to $new_version" -o pyproject.toml -o README.md
    git tag "v$new_version"
}

main() {
    case "$1" in
        "patch")
            bumpversion patch ;; 
        "minor")
            bumpversion minor ;;
        "major")
            bumpversion major ;;
         *)
            echo "usage: bumpversion (patch|minor|major)"
            exit 1
            ;;
    esac
}

main $@
