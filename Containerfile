ARG DOTFILES_IMAGE=sabas0ba/nixos
FROM ${DOTFILES_IMAGE}

ARG DOTFILES_REVISION=fc4cdecc02a6a95c81a259549d3fb9e7df18bb8f
LABEL io.github.sabas0ba.dotfiles-revision=${DOTFILES_REVISION}

ENV TANG_PRIMER_PROFILE=/nix/var/nix/profiles/tang-primer-20k-case
WORKDIR /workspace

COPY flake.nix flake.lock /opt/tang-primer-20k-case/
RUN nix develop /opt/tang-primer-20k-case --profile "$TANG_PRIMER_PROFILE" --command true \
  && rm -rf /root/.cache/nix

ENTRYPOINT ["nix", "develop", "/nix/var/nix/profiles/tang-primer-20k-case", "--command"]
CMD ["bash"]
